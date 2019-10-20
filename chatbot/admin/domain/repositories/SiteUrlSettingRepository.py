from abc import ABCMeta, abstractclassmethod
from chatbot.models.SiteUrlSetting import SiteUrlSettingModel


class ISiteUrlSettingRepository(metaclass=ABCMeta):
    @abstractclassmethod
    def get_list(self) -> list:
        pass

    @abstractclassmethod
    def find_by_id(self, id: int) -> SiteUrlSettingModel:
        pass

    @abstractclassmethod
    def save(self, url_setting: SiteUrlSettingModel):
        pass
