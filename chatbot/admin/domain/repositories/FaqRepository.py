from abc import ABCMeta, abstractclassmethod
from chatbot.models.Faq import FaqModel


class IFaqRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list_by_faq_list_id(self, faq_list_ld: int) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: int) -> FaqModel:
        pass

    @abstractclassmethod
    def find_by_question(self, question: str, faq_list_id: int):
        pass

    @abstractclassmethod
    def save(self, faq: FaqModel):
        pass
