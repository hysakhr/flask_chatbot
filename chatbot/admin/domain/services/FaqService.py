from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.models.Faq import FaqModel


class FaqService:
    def __init__(self, faq_repository: IFaqRepository):
        self.faq_repository = faq_repository

    def get_faqs_by_faq_list_id(self, faq_list_id: int) -> list:
        return self.faq_repository.get_list_by_faq_list_id(faq_list_id)

    def find_by_id(self, id: int) -> FaqModel:
        return self.faq_repository.find_by_id(id)

    def save(self, faq: FaqModel):
        return self.faq_repository.save(faq)
