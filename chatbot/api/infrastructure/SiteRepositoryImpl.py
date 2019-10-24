from chatbot.api.domain.repositories.SiteRepository import ISiteRepository
from chatbot.models.Site import SiteModel

from chatbot.database import db


class SiteRepositoryImpl(ISiteRepository):
    def find_by_id(self, id: int) -> SiteModel:
        return db.session.query(SiteModel).get(id)
