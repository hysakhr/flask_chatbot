FROM python:3.7

ADD . /flask_chatbot/chatbot
WORKDIR /flask_chatbot/chatbot
RUN pip install -r requirements.txt

WORKDIR /flask_chatbot
CMD flask run --port 5000 --host 0.0.0.0