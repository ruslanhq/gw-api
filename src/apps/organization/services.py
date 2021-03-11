from sqlalchemy import text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.base_services import BaseManager
from src.core.paginations import PagePagination
from . import models


class OrganizationManager(BaseManager):
    use_pagination = False
    pagination_class = PagePagination

    async def search_organizations(
            self, db: AsyncSession, page, title, law_address,
            status_organization, date_of_register
    ):
        filter_data = self.get_filter_dict(
            status_organization=status_organization, law_address=law_address,
            date_of_register=date_of_register
        )

        # through here criteria kwargs and use filter/ordering params
        queryset = (
            select(models.Organization)
            .filter_by(**filter_data)
            .outerjoin(models.Requisite)
            .outerjoin(models.Owner)
        )
        if title:
            queryset = queryset.filter(
                text(f"MATCH (organizations.title) AGAINST ('{title}')")
            )

        return await self.get_list(
            db=db, queryset=queryset, page=page
        )

    async def get_organization_detail(self, db: AsyncSession, pk: int):
        queryset = (
            select(models.Organization)
            .outerjoin(models.Requisite)
            .outerjoin(models.Owner)
            .filter(models.Organization.id == pk)
        )
        return await self.result(db=db, queryset=queryset, to_instance=True)

    @staticmethod
    def get_filter_dict(**kwargs):
        filters = {}
        for (key, value) in kwargs.items():
            if value is not None:
                filters[key] = value
        return filters
