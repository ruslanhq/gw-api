from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Json, validator

from src.core import airflow_dags as AF
from src.core.base_schemas import (
    RequisitesBase, OwnerBase, OrganizationBase, UserBase
)


class OrganizationStatus(Enum):
    operating = 1
    is_liquidation = 2
    liquidated = 3
    process_of_bankruptcy = 4
    process_of_reorganization = 5


class SearchStatus(Enum):
    success = 1
    running = 2
    failed = 3


class RequisiteSchema(RequisitesBase):
    id: int
    org_id: int


class OwnerSchema(OwnerBase):
    id: int
    org_id: int


class OrganizationSchema(OrganizationBase):
    id: Optional[int]


class QueryFilterSchema(BaseModel):

    @validator('query')
    def check_query(cls, value):
        if isinstance(value, int):
            raise ValueError('Query must be str type')
        if isinstance(value, str) and len(value) < 3:
            raise ValueError('Query must be 3 or more characters')
        return value

    query: str


class DagQuerySchema(QueryFilterSchema):

    @validator('dag_id')
    def check_dag_id(cls, value):
        if not AF.AirFlowDags().validate_dag_id_sync(dag_id=value):
            raise ValueError('dag_id should be in the list of available dags')
        return value

    dag_id: str


class SearchSchema(BaseModel):
    uuid: str
    user: str
    date: datetime
    user: UserBase
    metadata: Json = None
    query: QueryFilterSchema
    dag_id: DagQuerySchema

    class Config:
        orm_mode = True
