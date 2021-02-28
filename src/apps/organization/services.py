from sqlalchemy import func
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_services import BaseManager
from src.core.paginations import PagePagination
from . import models


class OrganizationManager(BaseManager):
    use_pagination = False
    pagination_class = PagePagination

    async def search_organizations(self, db: AsyncSession, page):
        # through here criteria kwargs and use filter/ordering params
        queryset = (
            select(models.Organization, func.count())
            .outerjoin(models.Requisite)
            .outerjoin(models.Owner)
        )
        return await self.get_list(
            db=db, model_klass=models.Organization, queryset=queryset, page=page
        )

    async def get_organization_detail(self, db: AsyncSession, pk: int):
        queryset = (
            select(models.Organization)
            .outerjoin(models.Requisite)
            .outerjoin(models.Owner)
            .filter(models.Organization.id == pk)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)
