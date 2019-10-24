import re

from chatbot.api.domain.repositories.SiteRepository import ISiteRepository
from chatbot.models.SiteUrlSetting import URL_PATTERN_DEFALT_ID
from chatbot.models.SiteUrlSetting import SiteUrlSettingModel


class SiteService:
    def __init__(self, site_repository: ISiteRepository):
        self.site_repository = site_repository

    def search_bot_id(self, site_id: int, url: str):
        site = self.site_repository.find_by_id(id=site_id)

        default_bot_id = 0
        for url_setting in site.url_settings:
            if url_setting.url_pattern == URL_PATTERN_DEFALT_ID:
                default_bot_id = url_setting.bot_id
                continue

            result = re.match(url_setting.url_pattern, url)
            if result:
                return url_setting.bot_id

        if default_bot_id == 0:
            raise Exception('bot_id not found')

        return default_bot_id

    def find_url_setting(self, site_id: int, url: str) -> SiteUrlSettingModel:
        site = self.site_repository.find_by_id(id=site_id)

        default_url_setting = None
        for url_setting in site.url_settings:
            if url_setting.url_pattern == URL_PATTERN_DEFALT_ID:
                default_url_setting = url_setting
                continue

            result = re.match(url_setting.url_pattern, url)
            if result:
                return url_setting

        if default_url_setting is None:
            raise Exception('url_setting not found')

        return default_url_setting
