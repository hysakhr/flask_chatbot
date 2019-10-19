from abc import ABCMeta, abstractclassmethod
from chatbot.models.Site import SiteModel


class ISiteRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list(self) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: int) -> SiteModel:
        pass

    @abstractclassmethod
    def save(self, site: SiteModel):
        pass
