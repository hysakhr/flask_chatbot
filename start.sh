#!/bin/bash

cd /flask_chatbot/chatbot
npm run watch &

cd /flask_chatbot
# flask db upgrade
flask run --port 5000 --host 0.0.0.0