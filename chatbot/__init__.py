import os

from flask import Flask
from flask_injector import FlaskInjector

from chatbot.database import init_db
from chatbot.binds import configure


def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
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

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # route setting
    from chatbot.routes import routes_setting
    routes_setting(app)

    # DI
    FlaskInjector(app=app, modules=[configure])

    return app
