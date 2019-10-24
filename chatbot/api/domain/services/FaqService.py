from chatbot.api.domain.repositories.FaqRepository import IFaqRepository
from chatbot.models.Faq import FaqModel


class FaqService:
    def __init__(self, faq_repository: IFaqRepository):
        self.faq_repository = faq_repository

    def find_by_id(self, id: int) -> FaqModel:
        return self.faq_repository.find_by_id(id)

    def get_list_by_ids(self, ids: list) -> list:
        return self.faq_repository.get_list_by_ids(ids)
