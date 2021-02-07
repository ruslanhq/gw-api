from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.apps.organization.schemas import OrganizationSchema
from src.apps.organization.services import OrganizationManager
from src.core.database import get_db_instance
from src.core.enums import HTTPErrorEnum

router = InferringRouter(
    prefix='organization',
    tags=['organization', 'api', 'schema'],
)


@cbv(router)
class OrganizationViewSet(OrganizationManager):
    name = 'organization'
    use_pagination = True
    session: Session = Depends(get_db_instance)

    @router.get('/{pk}', response_model=OrganizationSchema)
    async def detail_organization(self, pk: int) -> OrganizationSchema:
        item = self.get_organization_detailt(db=self.session, pk=pk)
        if not item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=HTTPErrorEnum.instance_not_found.value % self.name
            )
        return OrganizationSchema.from_orm(item)
