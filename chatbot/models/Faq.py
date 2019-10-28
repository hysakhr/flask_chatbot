from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

# class 定義せずに many to many 用 tableを定義
# metadata は不要でした
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/
# 検索するとTable class のコンストラクタ第2引数に metadata を渡しているものが多数出てきたので
# 記述していたがうまく行かなかった
faqs_faqs_table = db.Table(
    'faqs_faqs',
    db.Column(
        'faq_id',
        db.Integer,
        db.ForeignKey('faqs.id')),
    db.Column(
        'faq_list_id',
        db.Integer,
        db.ForeignKey('faq_lists.id')),
    db.Column(
        'question',
        db.Text))


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

    faq_list = relationship(
        'FaqListModel',
        back_populates='faqs', foreign_keys=[faq_list_id])

    related_faqs = relationship(
        'FaqModel',
        secondary=faqs_faqs_table,
        primaryjoin=id == faqs_faqs_table.c.faq_id,
        secondaryjoin='and_(faqs_faqs.c.faq_list_id==FaqModel.faq_list_id, faqs_faqs.c.question==FaqModel.question)')

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

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'

    def get_enable_related_faqs(self):
        return [faq for faq in self.related_faqs if faq.enable_flag]
