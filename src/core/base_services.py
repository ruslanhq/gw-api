from typing import ClassVar

from sqlalchemy.orm import Session

from .paginations import PagePagination


class BaseManager:
    use_pagination = False
    pagination_class = PagePagination

    def _get_list(self, db: Session, klass: ClassVar, page=1):
        query = db.query(klass).all()
        if self.use_pagination:
            items = self.pagination_class.get_query(query=query)
            total = query.order_by(None).count()
            return self.pagination_class(items, page, page, total)

        return query

    @staticmethod
    def get_instance_detail(db: Session, model, pk: int, joins=[]):
        return db.query(model).join(*joins).filter_by(id=pk).first()
