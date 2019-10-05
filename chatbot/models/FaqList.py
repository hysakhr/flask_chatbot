from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship

from chatbot.models.Faq import FaqModel
from chatbot.models.Bot import BotModel


class FaqListModel(db.Model):
    __tablename__ = 'faq_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)
    faqs = relationship('FaqModel', back_populates='faq_list')
    bots = relationship('BotModel', back_populates='faq_list')

    def __init__(self, name):
        self.name = name
