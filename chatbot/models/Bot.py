from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship


class BotModel(db.Model):
    __tablename__ = 'bots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    fitted_model_path = db.Column(db.Text, nullable=False)
    faq_list_id = db.Column(
        db.Integer,
        db.ForeignKey('faq_lists.id'),
        nullable=False)
    enable_flag = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    faq_list = relationship('FaqListModel', back_populates='bots')

    def __init__(
            self,
            name,
            fitted_model_path,
            faq_list_id,
            enable_flag=False):
        self.name = name
        self.fitted_model_path = fitted_model_path
        self.faq_list_id = faq_list_id
        self.enable_flag = enable_flag
