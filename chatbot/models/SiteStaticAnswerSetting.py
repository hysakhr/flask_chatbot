from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

from chatbot.models.StaticAnswer import StaticAnswerModel


class SiteStaticAnswerSettingModel(db.Model):
    __tablename__ = 'site_static_answer_settings'

    id = db.Column(db.Integer, primary_key=True)
    site_url_id = db.Column(
        db.Integer,
        db.ForeignKey('site_url_settings.id'),
        nullable=False)
    key = db.Column(db.Text, nullable=False)
    static_answer_id = db.Column(
        db.Integer,
        db.ForeignKey('static_answers.id'),
        nullable=False)
    enable_flag = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    site_url = relationship('SiteUrlSettingModel')
    static_answer = relationship('StaticAnswerModel')

    def __init__(self):
        self.url_pattern = ''
        self.enable_flag = False

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'
