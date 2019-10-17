from chatbot.admin.domain.repositories.StaticAnswerRepository import IStaticAnswerRepository
from chatbot.models.StaticAnswer import StaticAnswerModel


class StaticAnswerService:
    def __init__(self, static_answer_repository: IStaticAnswerRepository):
        self.static_answer_repository = static_answer_repository

    def get_new_obj(self, bot_id: int):
        return StaticAnswerModel(
            name='',
            answer='',
            bot_id=bot_id)

    def get_static_answers_by_bot_id(self, bot_id: int) -> list:
        return self.static_answer_repository.get_list_by_bot_id(
            bot_id)

    def find_by_id(self, id: int) -> StaticAnswerModel:
        return self.static_answer_repository.find_by_id(id)

    def save(self, static_answer: StaticAnswerModel):
        return self.static_answer_repository.save(static_answer)
