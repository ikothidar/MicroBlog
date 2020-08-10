import os
# from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
# load_dotenv(os.path.join(basedir, 'env'))


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

    LANGUAGES = ['en', 'es']

    MS_TRANSLATOR_KEY = os.environ.get('MS_TRANSLATOR_KEY')

    POSTS_PER_PAGE = 20

    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')