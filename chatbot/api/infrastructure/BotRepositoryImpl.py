from chatbot.api.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel

from chatbot.database import db


class BotRepositoryImpl(IBotRepository):
    def find_by_id(self, id: int) -> BotModel:
        return db.session.query(BotModel).get(id)
