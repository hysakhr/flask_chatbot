from chatbot.admin.domain.repositories.StaticAnswerRepository import IStaticAnswerRepository
from chatbot.models.StaticAnswer import StaticAnswerModel
from chatbot.database import db


class StaticAnswerRepositoryImpl(IStaticAnswerRepository):
    def get_list_by_bot_id(self, bot_id: int) -> list:
        return db.session.query(StaticAnswerModel).filter(
            StaticAnswerModel.bot_id == bot_id).order_by(
            StaticAnswerModel.id).all()

    def find_by_id(self, id: int) -> StaticAnswerModel:
        return db.session.query(StaticAnswerModel).get(id)

    def save(self, static_answer: StaticAnswerModel):
        db.session.add(static_answer)
        return db.session.commit()
