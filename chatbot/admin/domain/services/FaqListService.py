from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.FaqList import FaqListModel


class FaqListService:
    def __init__(self, faq_list_repository: IFaqListRepository):
        self.faq_list_repository = faq_list_repository

    def get_faq_lists(self):
        faq_lists = self.faq_list_repository.get_list()
        return faq_lists

    def find_by_id(
            self,
            id: int):
        faq_list = self.faq_list_repository.find_by_id(id)
        return faq_list

    def find_by_name(
            self,
            name: str):
        faq_list = self.faq_list_repository.find_by_name(name)
        return faq_list

    def save(self, faq_list: FaqListModel):
        return self.faq_list_repository.save(faq_list)
