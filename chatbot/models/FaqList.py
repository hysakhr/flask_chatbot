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
    start_faq_id = db.Column(
        db.Integer,
        db.ForeignKey('faqs.id'),
        nullable=True)
    not_found_faq_id = db.Column(
        db.Integer,
        db.ForeignKey('faqs.id'),
        nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    faqs = relationship('FaqModel', primaryjoin=id == FaqModel.faq_list_id)
    bot = relationship(
        'BotModel',
        back_populates='faq_lists',
        foreign_keys=[bot_id])
    start_faq = relationship('FaqModel',
                             primaryjoin=start_faq_id == FaqModel.id)
    not_found_faq = relationship('FaqModel',
                                 primaryjoin=not_found_faq_id == FaqModel.id)

    def __init__(self, bot_id: int, name: str = ''):
        self.name = name
        self.bot_id = bot_id
