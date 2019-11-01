FROM python:3.7

ADD . /flask_chatbot/chatbot
WORKDIR /flask_chatbot/chatbot
RUN pip install -r requirements.txt

RUN apt update && apt upgrade -y
RUN apt install -y nodejs npm
RUN npm install
RUN apt install -y mecab mecab-ipadic-utf8 libmecab-dev swig

WORKDIR /flask_chatbot
CMD sh start.sh