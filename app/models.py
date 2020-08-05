from flask import url_for
from datetime import datetime
from time import time

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login, app

from hashlib import md5

import jwt

followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship("Post", backref="author", lazy="dynamic")

    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    messages_sent = db.relationship('Message',
                                    foreign_keys='Message.sender_id',
                                    backref='author',
                                    lazy='dynamic')
    message_received = db.relationship('Message',
                                       foreign_keys='Message.recipient_id',
                                       backref='recipient',
                                       lazy='dynamic')
    last_message_read_time = db.Column(db.DateTime)

    def __repr__(self):
        return "<User {}>".format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode("utf-8")).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(
            digest, size)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0

    def followed_post(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)

        own = Post.query.filter_by(user_id=self.id)

        return followed.union(own).order_by(Post.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in
            },
            app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token,
                            app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    # def to_dict(self, include_email=False):
    #     data = {
    #         'id': self.id,
    #         'username': self.username,
    #         'last_seen': self.last_seen.isoformat() + 'Z',
    #         'about_me': self.about_me,
    #         'post_count': self.posts.count(),
    #         'follower_count': self.followers.count(),
    #         'followed_count': self.followed.count(),
    #         '_links': {
    #             'self': url_for('api.get_user', id=self.id),
    #             'followers': url_for('api.get_followers', id=self.id),
    #             'followed': url_for('api.get_followed', id=self.id),
    #             'avatar': self.avatar(128)
    #         }
    #     }
    #     if include_email:
    #         data['email'] = self.email

    #     return data

    # def from_dict(self, data, new_user=False):
    #     for field in ['username', 'email', 'about_me']:
    #         if field in data:
    #             setattr(self, field, data[field])
    #     if new_user and 'password' in data:
    #         self.set_password(data['password'])

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return Message.query.filter_by(recipient=self).filter(
            Message.timestamp > last_read_time).count()


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return "<Post {}>".format(self.body)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recipient_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Message {}>'.format(self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
