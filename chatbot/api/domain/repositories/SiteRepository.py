from abc import ABCMeta, abstractclassmethod
from chatbot.models.Site import SiteModel


class ISiteRepository(metaclass=ABCMeta):

    @abstractclassmethod
    def find_by_id(self, id: int) -> SiteModel:
        pass
