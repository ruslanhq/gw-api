from sqlalchemy.orm import Session

from src.core.base_services import BaseManager
from src.core.paginations import PagePagination
from . import models


class OrganizationManager(BaseManager):
    use_pagination = False
    pagination_class = PagePagination

    def search_organization(self, db: Session, page):
        return self._get_list(db=db, klass=models.Organization, page=page)

    @staticmethod
    def get_organization_detail(db: Session, pk: int):
        return db.query(models.Organization).join(
            models.Owner, models.Requisite
        ).filter_by(id=pk).first()
