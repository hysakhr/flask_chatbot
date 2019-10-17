from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

FIX_NAME = ['start', 'not_found']

# class 定義せずに many to many 用 tableを定義
static_answers_faqs_table = db.Table(
    'static_answers_faqs',
    db.Column(
        'static_answer_id',
        db.Integer,
        db.ForeignKey('static_answers.id'),
        primary_key=True),
    db.Column(
        'faq_id',
        db.Integer,
        db.ForeignKey('faqs.id'),
        primary_key=True),
    extend_existing=True)


class StaticAnswerModel(db.Model):
    __tablename__ = 'static_answers'

    id = db.Column(db.Integer, primary_key=True)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    name = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    bot = relationship('BotModel', back_populates='static_answers')
    faqs = relationship(
        'FaqModel',
        secondary=static_answers_faqs_table,
        primaryjoin=id == static_answers_faqs_table.c.static_answer_id,
        secondaryjoin=id == static_answers_faqs_table.c.faq_id)

    def __init__(
            self,
            name,
            answer,
            bot_id):
        self.name = name
        self.answer = answer
        self.bot_id = bot_id

    @reconstructor
    def init_on_load(self):
        if self.name in FIX_NAME:
            self.is_name_fixed = True
        else:
            self.is_name_fixed = False
