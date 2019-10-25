from chatbot.admin.domain.repositories.FaqRepository import IFaqRepository
from chatbot.models.Faq import FaqModel
from chatbot.database import db


class FaqRepositoryImpl(IFaqRepository):
    def get_list_by_faq_list_id(self, faq_list_id: int) -> list:
        return db.session.query(FaqModel).filter(
            FaqModel.faq_list_id == faq_list_id).order_by(
            FaqModel.id).all()

    def find_by_id(self, id: int) -> FaqModel:
        return db.session.query(FaqModel).get(id)

    def find_by_question(self, question: str, faq_list_id: int):
        return db.session.query(FaqModel).filter(
            FaqModel.question == question).filter(
            FaqModel.faq_list_id == faq_list_id).one()

    def save(self, faq: FaqModel):
        db.session.add(faq)
        return db.session.commit()
