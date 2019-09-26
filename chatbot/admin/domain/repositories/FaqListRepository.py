from abc import ABCMeta, abstractclassmethod
from chatbot.models.FaqList import FaqListModel


class IFaqListRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def find(self, id: int) -> FaqListModel:
        pass

    @abstractclassmethod
    def save(self, FaqListModel):
        pass

    @abstractclassmethod
    def getList(self) -> list:
        pass
