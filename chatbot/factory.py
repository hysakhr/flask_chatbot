import os

from flask import (Flask, g)
from flask_injector import FlaskInjector

from chatbot.database import init_db
from chatbot.binds import configure
from chatbot.celery_utils import init_celery

PKG_NAME = os.path.dirname(os.path.realpath(__file__)).split('/')[-1]


def create_app(test_config=None, app_name=PKG_NAME, **kwargs):
    # create and configure the app
    app = Flask(
        app_name,
        instance_relative_config=True,
        instance_path='/flask_chatbot/chatbot/instance'
    )
    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        config_object_string = 'chatbot.config.DevelopmentConfig'
        if app.config['ENV'] == 'production':
            config_object_string = 'chatbot.config.ProductionConfig'
        elif app.config['ENV'] == 'test':
            config_object_string = 'chatbot.config.TestingConfig'

        app.config.from_object(config_object_string)
        # app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    init_db(app)
    if kwargs.get('celery'):
        init_celery(kwargs.get('celery'), app)

    # ensure the instance folder exists
    try:
        makedirs_not_exists(app.instance_path)
        makedirs_not_exists(app.config['FAQ_FILE_UPLOAD_DIR'])
        makedirs_not_exists(app.config['ML_VARS_DIR'])
    except OSError:
        pass

    # route setting
    from chatbot.routes import routes_setting
    routes_setting(app)

    # DI
    FlaskInjector(app=app, modules=[configure])

    return app


def makedirs_not_exists(path: str):
    if os.path.exists(path):
        return

    os.makedirs(path)
