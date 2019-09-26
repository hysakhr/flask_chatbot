from datetime import datetime
from chatbot.database import db


class FaqModel(db.Model):
    __tablename__ = 'faq'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    question_org = db.Column(db.Text, nullable=False)
    answer_org = db.Column(db.Text, nullable=False)
    faq_list_id = db.Column(db.Integer, nullable=False, db.ForeignKey('faq_list.id'))
    enable_flag = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Columt(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(
            self,
            id,
            question,
            answer,
            question_org,
            answer_org,
            faq_list_id,
            enable_flag,
            created_at,
            updated_at):
        self.id = id
        self.question = question
        self.answer = answer
        self.question_org = question_org
        self.answer_org = answer_org
        self.faq_list_id = faq_list_id
        self.enable_flag = enable_flag
        self.created_at = created_at
        self.updated_at = updated_at
