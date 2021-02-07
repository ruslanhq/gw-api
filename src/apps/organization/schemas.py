from enum import Enum

from src.core.base_schemas import (
    RequisitesBase, OwnerBase, OrganizationBase,
)


class OrganizationStatus(Enum):
    operating = 1
    is_liquidation = 2
    liquidated = 3
    process_of_bankruptcy = 4
    process_of_reorganization = 5


class RequisiteSchema(RequisitesBase):
    id: int
    org_id: int


class OwnerSchema(OwnerBase):
    id: int
    org_id: int


class OrganizationSchema(OrganizationBase):
    id: int
