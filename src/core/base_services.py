from typing import ClassVar

from sqlalchemy.orm import Session

from .paginations import PagePagination


class BaseManager:
    schema = None
    use_pagination = False
    pagination_class = PagePagination

    @staticmethod
    async def result(db: Session, queryset, to_instance=False):
        result = await db.stream(queryset)
        _scalar = result.scalars()
        return await (_scalar.first() if to_instance else _scalar.all())

    async def get_list(self, db: Session, queryset: ClassVar, page=1):
        if self.use_pagination:
            items = await self.result(
                db, self.pagination_class.get_query(query=queryset)
            )
            total = len(items)
            return self.pagination_class(items, page, page, total, self.schema)
        else:
            return await self.result(db=db, queryset=queryset)
