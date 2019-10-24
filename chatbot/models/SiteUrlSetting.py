from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

from chatbot.models.Bot import BotModel
from chatbot.models.SiteStaticAnswerSetting import SiteStaticAnswerSettingModel
from chatbot.models.StaticAnswer import StaticAnswerModel

URL_PATTERN_DEFALT_ID = 'サイトのデフォルト'
STATIC_ANSWER_NAMES = ['start', 'not_found']


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
    site_static_answer_settings = relationship(
        'SiteStaticAnswerSettingModel',
        back_populates='site_url_setting')

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

        # デフォルトの書き換え
        if self.url_pattern == URL_PATTERN_DEFALT_ID:
            self.url_pattern_editable = False
        else:
            self.url_pattern_editable = True

        # 固定回答
        self.static_answers = {}
        for static_answer_setting in self.site_static_answer_settings:
            key = static_answer_setting.key
            name = static_answer_setting.static_answer_name
            self.static_answers[key] = name

    def get_static_answer(self, key: str) -> StaticAnswerModel:
        static_answer_name = ''
        for setting in self.site_static_answer_settings:
            if setting.key == key:
                static_answer_name = setting.static_answer_name
                break
        else:
            raise Exception(
                'static_answer_name not found. (key: {})'.format(key))

        for static_answer in self.bot.static_answers:
            if static_answer.name == static_answer_name:
                return static_answer

        raise Exception(
            'static_answer not found.(name: {})'.format(static_answer_name))
