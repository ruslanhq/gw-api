from typing import ClassVar

from sqlalchemy.orm import Session

from .paginations import PagePagination


class BaseManager:
    use_pagination = False
    pagination_class = PagePagination

    @staticmethod
    async def result(db: Session, queryset, to_instance=False):
        result = await db.stream(queryset)
        _scalar = result.scalars()
        return await (_scalar.first() if to_instance else _scalar.all())

    async def _get_list(self, db: Session, queryset: ClassVar, page=1):
        query = await self.result(db=db, queryset=queryset)
        if self.use_pagination:
            items = await self.pagination_class.get_query(query=query)
            total = await self.result(queryset.order_by(None).count())
            return self.pagination_class(items, page, page, total)

        return query

    @staticmethod
    async def get_instance_detail(db: Session, model, pk: int, joins=[]):
        return await db.query(model).join(*joins).filter_by(id=pk).first()
