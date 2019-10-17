from abc import ABCMeta, abstractclassmethod
from chatbot.models.StaticAnswer import StaticAnswerModel


class IStaticAnswerRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list_by_bot_id(self, bot_id: int) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: int) -> StaticAnswerModel:
        pass

    @abstractclassmethod
    def save(self, static_answer: StaticAnswerModel):
        pass
