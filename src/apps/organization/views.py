from datetime import date

from fastapi import Depends, HTTPException, Query
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_404_NOT_FOUND
from chadutils.sso.jwt_auth import JwtUser

from src.apps.organization.dependencies import get_auth_header
from src.apps.organization.schemas import (
    OrganizationSchema, DagQuerySchema, OrganizationStatus,
)
from src.apps.organization.services import OrganizationManager
from src.core.airflow_dags import AirFlowDags
from src.core.base_schemas import ResponseSchema
from src.core.database import get_db_instance
from src.core.enums import HTTPErrorEnum
from src.settings import settings

router = InferringRouter(tags=['api'])


@cbv(router)
class OrganizationViewSet(OrganizationManager):
    use_pagination = True
    name = 'Organization'
    schema = OrganizationSchema
    session: AsyncSession = Depends(get_db_instance)

    @router.get('/organization/{pk}', response_model=OrganizationSchema)
    async def detail_organization(self, pk: int) -> OrganizationSchema:
        item = await self.get_organization_detail(db=self.session, pk=pk)
        if not item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=HTTPErrorEnum.instance_not_found.value % self.name
            )
        return self.schema.from_orm(item)

    @router.get('/organizations/', response_model=ResponseSchema)
    async def list_criteria_organizations(
            self, page: int = Query(1, gt=0),
            title: str = Query(None, min_length=3),
            law_address: str = Query(None, min_length=3),
            status_organization: int = (
                    Query(OrganizationStatus.operating.value, gt=0, lt=6)
            ),
            date_of_register: date = Query(None, description=f'{date.today()}')
    ) -> ResponseSchema:
        # use a custom schema to small response
        # self.schema = OrganizationListSchema

        response = await self.search_organizations(
            db=self.session, page=page, title=title,
            status_organization=status_organization,
            date_of_register=date_of_register,
            law_address=law_address,
        )
        return ResponseSchema.from_orm(response)


@cbv(router)
class QuerySearchView:
    session: AsyncSession = Depends(get_db_instance)

    @router.post('/search')
    async def dag_start(
            self, payload: DagQuerySchema,
            auth_header: str = Depends(get_auth_header)
    ):
        user_id = JwtUser.get_jwt_user(
            auth_header, settings.main.SECRET_KEY.get_secret_value()
        )

        await (
            AirFlowDags(db=self.session)
            .trigger_dag(payload.dag_id, payload.query, user_id)
        )
        return payload

    @router.get('/dag_list')
    async def get_list(self):
        return await AirFlowDags().get_list_dags()

    @router.get('/status_dag/{dag_id}')
    async def get_status_dag(self, dag_id):
        return await AirFlowDags().get_status_dag(dag_id)

    @router.get('/status_dag_run/{dag_id}/{dag_run_id}')
    async def get_dag_run_status(self, dag_id, dag_run_id):
        return (
            await AirFlowDags(db=self.session)
            .get_status_dagrun(dag_id, dag_run_id)
        )
