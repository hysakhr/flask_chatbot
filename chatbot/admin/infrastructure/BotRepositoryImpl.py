from chatbot.admin.domain.repositories.BotRepository import IBotRepository
from chatbot.models.Bot import BotModel
from chatbot.database import db


class BotRepositoryImpl(IBotRepository):
    def get_list_by_faq_list_id(self, faq_list_id: int) -> list:
        return db.session.query(BotModel).filter(
            BotModel.faq_list_id == faq_list_id).order_by(
            BotModel.id).all()

    def get_list(self) -> list:
        return db.session.query(BotModel).order_by(
            BotModel.id).all()

    def find_by_id(self, id: int) -> BotModel:
        return db.session.query(BotModel).get(id)

    def save(self, bot: BotModel):
        db.session.add(bot)
        return db.session.commit()
