import os

from celery import Celery
from chatbot.config import get_config


def make_cerely(app_name=__name__):
    config = get_config(os.getenv('FLASK_ENV', 'development'))
    return Celery(
        app_name,
        backend=config.CELERY_RESULT_BACKEND,
        broker=config.CELERY_BROKER_URL)


celery = make_cerely()
