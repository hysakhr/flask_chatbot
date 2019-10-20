from chatbot.admin.domain.repositories.SiteUrlSettingRepository import ISiteUrlSettingRepository
from chatbot.models.SiteUrlSetting import SiteUrlSettingModel
from chatbot.database import db


class SiteUrlSettingRepositoryImpl(ISiteUrlSettingRepository):
    def get_list(self) -> list:
        return db.session.query(SiteUrlSettingModel).order_by(
            SiteUrlSettingModel.id).all()

    def find_by_id(self, id: int) -> SiteUrlSettingModel:
        return db.session.query(SiteUrlSettingModel).get(id)

    def save(self, url_setting: SiteUrlSettingModel):
        db.session.add(url_setting)
        return db.session.commit()
