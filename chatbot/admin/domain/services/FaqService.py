from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository


class FaqService:
    def __init__(self):
        pass

    def getFqaList(self, faq_list_repository: IFaqListRepository):
        faq_list = faq_list_repository.getList()
        return faq_list
