from chatbot import factory
import chatbot

app = factory.create_app(celery=chatbot.celery)
app.run()
