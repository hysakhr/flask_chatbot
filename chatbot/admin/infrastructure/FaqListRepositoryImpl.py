from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.FaqList import FaqListModel
from chatbot.database import db


class FaqListRepositoryImpl(IFaqListRepository):
    def find(self, id: int) -> FaqListModel:
        pass

    def save(self, FaqListModel):
        pass

    def getList(self) -> list:
        return db.session.query(FaqListModel).all()
