from chatbot.admin.domain.repositories.SiteRepository import ISiteRepository

from chatbot.models.Site import SiteModel


class SiteService:
    def __init__(self, site_repository: ISiteRepository):
        self.site_repository = site_repository

    def get_new_obj(self) -> SiteModel:
        return SiteModel()

    def get_sites(self) -> list:
        return self.site_repository.get_list()

    def find_by_id(self, id: int) -> SiteModel:
        return self.site_repository.find_by_id(id)

    def add(self, site: SiteModel):
        self.site_repository.save(site)

    def edit(self, site: SiteModel):
        return self.site_repository.save(site)
