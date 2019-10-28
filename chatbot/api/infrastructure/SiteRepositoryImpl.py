from chatbot.api.domain.repositories.SiteRepository import ISiteRepository
from chatbot.models.Site import SiteModel

from chatbot.database import db


class SiteRepositoryImpl(ISiteRepository):
    def find_by_id(self, id: int) -> SiteModel:
        return db.session.query(SiteModel).filter(
            SiteModel.id == id).filter(
            SiteModel.enable_flag).one_or_none()
