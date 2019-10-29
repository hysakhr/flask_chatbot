from abc import ABCMeta, abstractclassmethod
from chatbot.models.TalkLog import TalkLogModel


class ITalkLogRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def add(self, talk_log: TalkLogModel):
        pass
