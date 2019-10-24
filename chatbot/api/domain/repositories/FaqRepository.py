from abc import ABCMeta, abstractclassmethod
from chatbot.models.Faq import FaqModel


class IFaqRepository(metaclass=ABCMeta):

    @abstractclassmethod
    def find_by_id(self, id: int) -> FaqModel:
        pass

    @abstractclassmethod
    def get_list_by_ids(self, ids: list) -> list:
        pass
