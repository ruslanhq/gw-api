from typing import ClassVar

from sqlalchemy.orm import Session

from . import models
from ...core.paginations import PagePagination


class OrganizationManager:
    use_pagination = False
    pagination_class = PagePagination

    def _get_list(self, db: Session, klass: ClassVar, page=1):
        query = db.query(klass).all()
        if self.use_pagination:
            items = self.pagination_class.get_query(query=query)
            total = query.order_by(None).count()
            return self.pagination_class(items, page, page, total)

        return query

    def search_organization(self, db: Session, page):
        return self._get_list(db=db, klass=models.Organization, page=page)

    @staticmethod
    def get_organization_detail(db: Session, pk: int):
        return db.query(models.Organization).join(
            models.Owner, models.Requisite
        ).filter_by(id=pk).first()
