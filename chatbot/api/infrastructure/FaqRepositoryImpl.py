from chatbot.api.domain.repositories.FaqRepository import IFaqRepository
from chatbot.models.Faq import FaqModel
from chatbot.database import db


class FaqRepositoryImpl(IFaqRepository):

    def find_by_id(self, id: int) -> FaqModel:
        return db.session.query(FaqModel).get(id)

    def get_list_by_ids(self, ids: list) -> list:
        faqs = db.session.query(FaqModel).filter(FaqModel.id.in_(ids)).all()

        ret = []
        for id in ids:
            for faq in faqs:
                if id == faq.id:
                    ret.append(faq)
                    break
        return ret
