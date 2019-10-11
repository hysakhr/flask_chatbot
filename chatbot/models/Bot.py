from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship, reconstructor

FITTED_STATE_NO_FIT = 0
FITTED_STATE_FITTING = 1
FITTED_STATE_FITTED = 2


class BotModel(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    fitted_model_path = db.Column(db.Text, nullable=False)
    faq_list_id = db.Column(
        db.Integer,
        db.ForeignKey('faq_lists.id'),
        nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    fitted_state = db.Column(
        db.Integer,
        nullable=False,
        default=FITTED_STATE_NO_FIT)
    enable_flag = db.Column(db.Boolean, nullable=False, default=False)

    faq_list = relationship(
        'FaqListModel',
        back_populates='bots',
        lazy='joined')

    def __init__(
            self,
            name,
            fitted_model_path,
            faq_list_id=None,
            fitted_state=FITTED_STATE_NO_FIT,
            enable_flag=False):
        self.name = name
        self.fitted_model_path = fitted_model_path
        self.faq_list_id = faq_list_id
        self.fitted_state = fitted_state
        self.fitted_state_label = '未学習'
        self.enable_flag = enable_flag

        if self.fitted_state == FITTED_STATE_FITTING:
            self.fitted_state_label = '学習中'
        elif self.fitted_state == FITTED_STATE_FITTED:
            self.fitted_state_label = '学習済'

    @reconstructor
    def init_on_load(self):
        # 有効無効のラベル
        if self.enable_flag:
            self.enable_label = '有効'
        else:
            self.enable_label = '無効'

        # 学習状態のラベル
        if self.fitted_state == FITTED_STATE_FITTING:
            self.fitted_state_label = '学習中'
        elif self.fitted_state == FITTED_STATE_FITTED:
            self.fitted_state_label = '学習済'
        else:
            self.fitted_state_label = '未学習'

        # 学習ボタンの活性条件
        self.fit_button_enable = True
        if self.faq_list_id is None or self.fitted_state == FITTED_STATE_FITTING:
            self.fit_button_enable = False
