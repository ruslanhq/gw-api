from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session
from starlette.status import HTTP_404_NOT_FOUND

from src.apps.organization.schemas import OrganizationSchema, DagQuerySchema
from src.apps.organization.services import OrganizationManager
from src.core.airflow_dags import AirFlowDags
from src.core.database import get_db_instance
from src.core.enums import HTTPErrorEnum

router = InferringRouter(tags=['api'])


@cbv(router)
class OrganizationViewSet(OrganizationManager):
    use_pagination = True
    schema = OrganizationSchema
    session: Session = Depends(get_db_instance)

    @router.get('/organization/{pk}', response_model=OrganizationSchema)
    async def detail_organization(self, pk: int) -> OrganizationSchema:
        item = await self.get_organization_detail(db=self.session, pk=pk)
        if not item:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=HTTPErrorEnum.instance_not_found.value % self.name
            )
        return self.schema.from_orm(item)

    @router.get('/organizations/')
    async def list_criteria_organizations(self) -> dict:
        response = await self.search_organizations(db=self.session, page=1)
        return response.meta_response()


@cbv(router)
class QuerySearchView:
    session: Session = Depends(get_db_instance)

    @router.post('/search', response_model=DagQuerySchema)
    async def dag_start(self, payload: DagQuerySchema):
        await (
            AirFlowDags(db=self.session)
            .trigger_dag(payload.dag_id, payload.query)
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
