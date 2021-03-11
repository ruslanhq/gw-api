from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.database import settings
from .paginations import PagePagination


class BaseManager:
    schema = None
    use_pagination = False
    pagination_class = PagePagination

    @staticmethod
    async def result(db: AsyncSession, queryset, to_instance=False):
        result = await db.stream(queryset)
        _scalar = result.scalars()
        return await (_scalar.first() if to_instance else _scalar.all())

    async def get_list(
            self, db: AsyncSession, queryset: ClassVar, page=1
    ):
        if self.use_pagination:
            total = len(await self.result(db, queryset))
            queryset = self.pagination_class.get_query(query=queryset, page=page)
            items = await self.result(
                db, self.pagination_class.get_query(query=queryset, page=page)
            )
            return self.pagination_class(
                items, page, settings.PAGE_SIZE, total, self.schema
            )
        else:
            return await self.result(db=db, queryset=queryset)
