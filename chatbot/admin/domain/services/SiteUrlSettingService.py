from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository

from chatbot.models.SiteUrlSetting import SiteUrlSettingModel, URL_PATTERN_DEFALT_ID


class SiteUrlSettingService:
    def __init__(self, site_url_setting_repository: ISiteUrlSettingRepository):
        self.site_url_setting_repository = site_url_setting_repository

    def get_new_obj(self, site_id: int) -> SiteUrlSettingModel:
        return SiteUrlSettingModel(site_id=site_id)

    def get_url_settings(self) -> list:
        return self.site_url_setting_repository.get_list()

    def find_by_id(self, id: int):
        return self.site_url_setting_repository.find_by_id(id)

    def add(self, url_setting: SiteUrlSettingModel):
        return self.site_url_setting_repository.save(url_setting)

    def edit(self, url_setting: SiteUrlSettingModel):
        if not url_setting.url_pattern_editable:
            url_setting.url_pattern = URL_PATTERN_DEFALT_ID

        return self.site_url_setting_repository.save(url_setting)
