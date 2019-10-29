from chatbot.api.domain.repositories.TalkLogReposiroty import ITalkLogRepository
from chatbot.models.TalkLog import TalkLogModel

from chatbot.database import db


class TalkLogRepositoryImpl(ITalkLogRepository):
    def add(self, talk_log: TalkLogModel):
        db.session.add(talk_log)
        return db.session.commit()
