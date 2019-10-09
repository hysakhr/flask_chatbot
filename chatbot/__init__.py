import os

from celery import Celery
from chatbot.config import get_config


def make_cerely(app_name=__name__):
    config = get_config(os.getenv('FLASK_ENV', 'development'))
    app = Celery(
        app_name,
        backend=config.CELERY['backend'],
        broker=config.CELERY['broker'],
        imports=config.CELERY['imports'])

    return app


celery = make_cerely()
