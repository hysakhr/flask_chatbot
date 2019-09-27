from chatbot.admin.domain.repositories.FaqListRepository import IFaqListRepository
from chatbot.models.FaqList import FaqListModel
from chatbot.database import db


class FaqListRepositoryImpl(IFaqListRepository):
    def find_by_id(self, id: int) -> FaqListModel:
        return db.session.query(FaqListModel).get(id)

    def find_by_name(self, name: str) -> FaqListModel:
        pass

    def save(self, faq_list: FaqListModel):
        db.session.add(faq_list)
        return db.session.commit()

    def get_list(self) -> list:
        return db.session.query(FaqListModel).order_by(
            FaqListModel.updated_at.desc()).all()
