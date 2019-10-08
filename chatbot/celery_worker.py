from chatbot import celery
from chatbot.factory import create_app
from chatbot.celery_utils import init_celery

app = create_app()
init_celery(celery, app)
