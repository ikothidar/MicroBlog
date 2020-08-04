import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'kjbshrgfdsjn'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 25
    MAIL_USE_TLS = True
    MAIL_USERNAME = '9bd0aa1baae267'
    MAIL_PASSWORD = 'c61e05da8e4075'
    ADMINS = ['ikothiadr@gmail.com']

    POSTS_PER_PAGE = 3

    LANGUAGES = ['en', 'es']