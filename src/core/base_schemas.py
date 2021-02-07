from datetime import date
from typing import List

from pydantic import BaseModel, Json


class RequisitesBase(BaseModel):
    type: str = None
    ogrn: int = None
    dates: date = None
    registrar: str = None
    address: Json = None
    reg_number: int = None
    name: str = None
    category: str = None

    class Config:
        orm_mode = True


class OwnerBase(BaseModel):
    first: str
    last: str
    middle: str

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    id_org: int
    title: str
    status_organization: int
    ogrn: int
    ogrn_date_from: date
    date_of_register: date
    law_address: Json
    owner: List[OwnerBase]
    owner_date_from: date
    inn_number: int
    kpp_number: int
    authorized_capital: str
    primary_occupation: str
    primary_occupation_code: int
    tax_authority: str
    tax_authority_date_from: date
    okpo: int
    okato: int
    oktmo: int
    okfs: int
    okogu: int
    requisites: List[RequisitesBase]

    class Config:
        orm_mode = True
