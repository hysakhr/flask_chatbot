from datetime import datetime
import json
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor
from flask import request

from chatbot.api.helpers.responses.Talk import TalkResponse


class TalkLogModel(db.Model):
    __tablename__ = 'talk_logs'

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer)
    bot_id = db.Column(db.Integer)
    session_id = db.Column(db.String(255))
    talk_type = db.Column(db.String(255))
    request_faq_id: db.Column(db.Integer)
    request_static_answer_name = db.Column(db.Text)
    request_query = db.Column(db.Text)
    user_agent = db.Column(db.Text)
    response_faq_id = db.Column(db.Integer)
    response_faqs = db.Column(db.Text)
    score = db.Column(db.Text)
    error_message = db.Column(db.Text)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    def __init__(
            self,
            request: request,
            response: TalkResponse = None,
            top_faq_info_list: list = None,
            bot_id: int = None,
            session_id: str = None):
        self.site_id = int(request.json['site_id'])
        self.bot_id = bot_id
        self.session_id = session_id
        self.talk_type = request.json['type']
        self.request_faq_id = request.json['faq_id'] if 'faq_id' in request.json else None
        self.request_static_answer_name = request.json['name'] if 'name' in request.json else None
        self.request_query = request.json['query'] if 'query' in request.json else None
        self.user_agent = request.headers.get('User-Agent')
        self.response_faq_id = response.answer.id if response.answer else None
        if response.faqs:
            faq_questions = [faq.question for faq in response.faqs]
            self.response_faqs = ','.join(faq_questions)
        if top_faq_info_list:
            dump_list = []
            for faq_info in top_faq_info_list:
                dump_list.append({
                    'faq_id': faq_info['faq_id'],
                    'question': faq_info['question'],
                    'score': faq_info['score']
                })
            self.score = json.dumps(dump_list, ensure_ascii=False)
        self.error_message = response.error_message
