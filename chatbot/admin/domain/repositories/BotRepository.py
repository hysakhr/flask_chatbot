from abc import ABCMeta, abstractclassmethod
from chatbot.models.Bot import BotModel


class IBotRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list_by_faq_list_id(self, faq_list_id: int) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: int) -> BotModel:
        pass

    @abstractclassmethod
    def save(self, bot: BotModel):
        pass
