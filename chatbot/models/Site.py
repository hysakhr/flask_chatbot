from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

from chatbot.models.SiteUrlSetting import SiteUrlSettingModel


class SiteModel(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    enable_flag = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    url_settings = relationship('SiteUrlSettingModel', back_populates='site')

    def __init__(self):
        self.name = ''
        self.enable_flag = False

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'
