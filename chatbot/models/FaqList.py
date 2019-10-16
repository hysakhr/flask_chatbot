from datetime import datetime
from chatbot.database import db
from sqlalchemy.orm import relationship

from chatbot.models.Faq import FaqModel
from chatbot.models.Bot import BotModel


class FaqListModel(db.Model):
    __tablename__ = 'faq_lists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    bot_id = db.Column(db.Integer, db.ForeignKey('bots.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    faqs = relationship('FaqModel', back_populates='faq_list')
    bot = relationship(
        'BotModel',
        back_populates='faq_lists',
        foreign_keys=[bot_id])

    def __init__(self, bot_id: int, name: str = ''):
        self.name = name
        self.bot_id = bot_id
