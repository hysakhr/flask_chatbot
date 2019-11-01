from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

from chatbot.models.SiteUrlSetting import SiteUrlSettingModel


class SiteModel(db.Model):
    __tablename__ = 'sites'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    enable_flag = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    url_settings = relationship('SiteUrlSettingModel', back_populates='site')

    def __init__(self, enable_flag: bool = True):
        self.name = ''
        self.enable_flag = enable_flag

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'

        # ボットが設定されているURL（デフォルト含む）があるか
        self.have_bot = False
        for url_setting in self.url_settings:
            if url_setting.bot_id:
                self.have_bot = True
                break
