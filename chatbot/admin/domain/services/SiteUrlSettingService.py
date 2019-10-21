from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository

from chatbot.models.SiteUrlSetting import SiteUrlSettingModel
from chatbot.models.SiteStaticAnswerSetting import SiteStaticAnswerSettingModel


class SiteUrlSettingService:
    def __init__(self, site_url_setting_repository: ISiteUrlSettingRepository):
        self.site_url_setting_repository = site_url_setting_repository

    def get_new_obj(self, site_id: int) -> SiteUrlSettingModel:
        return SiteUrlSettingModel(site_id=site_id)

    def get_url_settings(self) -> list:
        return self.site_url_setting_repository.get_list()

    def find_by_id(self, id: int):
        return self.site_url_setting_repository.find_by_id(id)

    def add(self, url_setting: SiteUrlSettingModel, static_answers):
        url_setting.site_static_answer_settings = []
        for k in static_answers:
            site_static_answer_setting = SiteStaticAnswerSettingModel(
                site_url_id=None, key=k, static_answer_name=static_answers[k])
            url_setting.site_static_answer_settings.append(
                site_static_answer_setting)

        return self.site_url_setting_repository.save(url_setting)

    def edit(self, url_setting: SiteUrlSettingModel, static_answers):
        for site_static_answer_setting in url_setting.site_static_answer_settings:
            k = site_static_answer_setting.key
            site_static_answer_setting.static_answer_name = static_answers[k]
        return self.site_url_setting_repository.save(url_setting)
