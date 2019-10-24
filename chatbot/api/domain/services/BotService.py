from chatbot.api.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel


class BotService:
    def __init__(self, bot_repository: IBotRepository):
        self.bot_repository = bot_repository

    def find_by_id(self, id: int) -> BotModel:
        return self.bot_repository.find_by_id(id)
