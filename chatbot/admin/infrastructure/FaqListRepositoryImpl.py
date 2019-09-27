from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.FaqList import FaqListModel
from chatbot.database import db


class FaqListRepositoryImpl(IFaqListRepository):
    def find_by_id(self, id: int) -> FaqListModel:
        return FaqListModel.query.get(id)

    def find_by_name(self, name: str) -> FaqListModel:
        pass

    def save(self, FaqListModel):
        db.session.add(FaqListModel)
        return db.session.commit()

    def get_list(self) -> list:
        return FaqListModel.query.order_by(FaqListModel.id).all()
        # return db.session.query(FaqListModel).all()
