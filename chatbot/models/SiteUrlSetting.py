from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

from chatbot.models.Bot import BotModel
from chatbot.models.SiteStaticAnswerSetting import SiteStaticAnswerSettingModel


class SiteUrlSettingModel(db.Model):
    __tablename__ = 'site_url_settings'

    id = db.Column(db.Integer, primary_key=True)
    url_pattern = db.Column(db.Text, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey('sites.id'), nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=True)
    enable_flag = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    site = relationship('SiteModel', back_populates='url_settings')
    bot = relationship('BotModel')
    static_answers = relationship('SiteStaticAnswerSettingModel')

    def __init__(self, site_id: int):
        self.site_id = site_id
        self.url_pattern = ''
        self.enable_flag = False

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'
