from datetime import date
from typing import List, Optional

from pydantic import BaseModel, EmailStr
from pydantic.schema import Enum


class RequisitesBase(BaseModel):
    id: int
    type: str = None
    ogrn: int = None
    req_dt: date = None
    registrar: str = None
    address: dict = None
    reg_number: int = None
    name: str = None
    category: str = None

    class Config:
        orm_mode = True


class OwnerBase(BaseModel):
    id: int
    first: Optional[str]
    last: Optional[str]
    middle: Optional[str]

    class Config:
        orm_mode = True


class OrganizationBase(BaseModel):
    title: Optional[str]
    external_id: Optional[int]
    status_organization: Optional[Enum]
    ogrn: Optional[int]
    ogrn_date_from: Optional[date]
    date_of_register: Optional[date]
    law_address: Optional[dict]
    owners: List[OwnerBase]
    owner_date_from: Optional[date]
    inn_number: Optional[int]
    kpp_number: Optional[int]
    authorized_capital: Optional[str]
    primary_occupation: Optional[str]
    primary_occupation_code: Optional[int]
    tax_authority: Optional[str]
    tax_authority_date_from: Optional[date]
    okpo: Optional[int]
    okato: Optional[int]
    oktmo: Optional[int]
    okfs: Optional[int]
    okogu: Optional[int]
    requisites: List[RequisitesBase]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr
    password: str
    phone: str

    class Config:
        orm_mode = True
