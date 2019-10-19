from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository
from chatbot.models.Site import SiteModel
from chatbot.database import db


class SiteRepositoryImpl(ISiteRepository):
    def get_list(self) -> list:
        return db.session.query(SiteModel).order_by(SiteModel.id).all()

    def find_by_id(self, id: int) -> SiteModel:
        return db.session.query(SiteModel).get(id)

    def save(self, site: SiteModel):
        db.session.add(site)
        return db.session.commit()
