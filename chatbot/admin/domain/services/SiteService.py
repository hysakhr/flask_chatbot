from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository

from chatbot.models.Site import SiteModel
from chatbot.models.SiteUrlSetting import SiteUrlSettingModel, URL_PATTERN_DEFALT_ID, STATIC_ANSWER_NAMES
from chatbot.models.SiteStaticAnswerSetting import SiteStaticAnswerSettingModel


class SiteService:
    def __init__(self, site_repository: ISiteRepository):
        self.site_repository = site_repository
        # self.site_url_setting_repository = site_url_setting_repositoryS

    def get_new_obj(self) -> SiteModel:
        return SiteModel()

    def get_sites(self) -> list:
        return self.site_repository.get_list()

    def find_by_id(self, id: int) -> SiteModel:
        return self.site_repository.find_by_id(id)

    def add(self, site: SiteModel):
        # サイトごとの設定のデフォルト
        site_url_setting = SiteUrlSettingModel(site_id=None)
        site_url_setting.url_pattern = URL_PATTERN_DEFALT_ID
        site_url_setting.site_static_answer_settings = []

        # 固定回答
        for name in STATIC_ANSWER_NAMES:
            site_static_answer_setting = SiteStaticAnswerSettingModel(
                site_url_id=None, key=name, static_answer_name=name)
            site_url_setting.site_static_answer_settings.append(
                site_static_answer_setting)

        site.url_settings = [site_url_setting]

        self.site_repository.save(site)

    def edit(self, site: SiteModel):
        return self.site_repository.save(site)
