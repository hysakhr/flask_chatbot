FROM python:3.7

ADD . /flask_chatbot/chatbot
WORKDIR /flask_chatbot/chatbot
RUN pip install -r requirements.txt

RUN apt update && apt upgrade -y
RUN apt install -y nodejs npm

WORKDIR /flask_chatbot
CMD sh start.sh