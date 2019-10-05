import os


class Config(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    FAQ_FILE_UPLOAD_DIR = '/flask_chatbot/chatbot/upload'
    ML_VARS_DIR = '/flask_chatbot/chatbot/ml_vars'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class DevelopmentConfig(Config):
    DEBUG = True

    # SQLAlchemy
    dbCOnfig = {
        'user': os.getenv('DB_USER', 'chatbot'),
        'password': os.getenv('DB_PASSWORD', 'chatbot'),
        'host': os.getenv('DB_HOST', 'mysql'),
        'database': os.getenv('DB_DATABASE', 'chatbot'),
    }
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8'.format(
        **dbCOnfig)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    TESTING = True
