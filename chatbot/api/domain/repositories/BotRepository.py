from abc import ABCMeta, abstractclassmethod
from chatbot.models.Bot import BotModel


class IBotRepository(metaclass=ABCMeta):

    @abstractclassmethod
    def find_by_id(self, id: int) -> BotModel:
        pass
