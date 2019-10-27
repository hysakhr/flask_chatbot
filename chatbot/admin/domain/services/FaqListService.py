from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.models.FaqList import FaqListModel


class FaqListService:
    def __init__(
            self,
            faq_list_repository: IFaqListRepository,
            faq_repository: IFaqRepository):
        self.faq_list_repository = faq_list_repository
        self.faq_repository = faq_repository

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

    def edit(self, faq_list: FaqListModel):
        if faq_list.start_faq_id:
            faq = self.faq_repository.find_by_id(faq_list.start_faq_id)
            faq_list.start_faq = faq

        if faq_list.not_found_faq_id:
            faq = self.faq_repository.find_by_id(faq_list.not_found_faq_id)
            faq_list.not_found_faq = faq

        return self.faq_list_repository.save(faq_list)
