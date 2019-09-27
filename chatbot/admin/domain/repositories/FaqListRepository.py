from abc import ABCMeta, abstractclassmethod
from chatbot.models.FaqList import FaqListModel


class IFaqListRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def find_by_id(self, id: int) -> FaqListModel:
        pass

    @abstractclassmethod
    def find_by_name(self, name: str) -> FaqListModel:
        pass

    @abstractclassmethod
    def save(self, faq_list: FaqListModel):
        pass

    @abstractclassmethod
    def get_list(self) -> list:
        pass
