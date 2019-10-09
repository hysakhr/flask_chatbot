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
        nullable=False)
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

    faq_list = relationship('FaqListModel', back_populates='bots')

    def __init__(
            self,
            name,
            fitted_model_path,
            faq_list_id,
            fitted_state=FITTED_STATE_NO_FIT):
        self.name = name
        self.fitted_model_path = fitted_model_path
        self.faq_list_id = faq_list_id
        self.fitted_state = fitted_state
        self.fitted_state_label = '未学習'

        if self.fitted_state == FITTED_STATE_FITTING:
            self.fitted_state_label = '学習中'
        elif self.fitted_state == FITTED_STATE_FITTED:
            self.fitted_state_label = '学習済'

    @reconstructor
    def init_on_load(self):
        self.fitted_state_label = '未学習'

        if self.fitted_state == FITTED_STATE_FITTING:
            self.fitted_state_label = '学習中'
        elif self.fitted_state == FITTED_STATE_FITTED:
            self.fitted_state_label = '学習済'
