from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship


class FaqModel(db.Model):
    __tablename__ = 'faqs'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    question_org = db.Column(db.Text, nullable=False)
    answer_org = db.Column(db.Text, nullable=False)
    faq_list_id = db.Column(
        db.Integer,
        db.ForeignKey('faq_lists.id'),
        nullable=False)
    enable_flag = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    faq_list = relationship('FaqListModel', back_populates='faqs')

    def __init__(
            self,
            question,
            answer,
            question_org,
            answer_org,
            faq_list_id,
            enable_flag=True):
        self.question = question
        self.answer = answer
        self.question_org = question_org
        self.answer_org = answer_org
        self.faq_list_id = faq_list_id
        self.enable_flag = enable_flag
