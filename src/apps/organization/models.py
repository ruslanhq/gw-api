from sqlalchemy import (
    Column, ForeignKey, Integer, String,
    Date, JSON, Enum, DateTime,
)
from sqlalchemy.orm import relationship

import uuid
from src.apps.organization.schemas import OrganizationStatus, SearchStatus
from src.core.database import Base
from src.core.fields_sqlalchemy.types.uuid import UUIDType


class Organization(Base):
    __tablename__ = 'organizations'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    external_id = Column(Integer, unique=True, index=True)
    title = Column(String(255))
    status_organization = Column(
        Enum(OrganizationStatus), index=True
    )
    ogrn = Column(Integer)
    ogrn_date_from = Column(Date)
    date_of_register = Column(Date)
    law_address = Column(JSON)
    owner_date_from = Column(Date)
    inn_number = Column(Integer)
    kpp_number = Column(Integer)
    authorized_capital = Column(String(255))
    primary_occupation = Column(String(255))
    primary_occupation_code = Column(Integer)
    tax_authority = Column(String(255))
    tax_authority_date_from = Column(Date)
    okpo = Column(Integer)
    okato = Column(Integer)
    oktmo = Column(Integer)
    okfs = Column(Integer)
    okogu = Column(Integer)


class Requisite(Base):
    __tablename__ = 'requisites'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(255), index=True)
    ogrn = Column(Integer)
    req_dt = Column(Date, index=True)
    registrar = Column(String(255))
    address = Column(JSON)
    reg_number = Column(Integer)
    name = Column(String(255))
    category = Column(String(255))
    org_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship(
        Organization, backref='requisites', lazy='joined'
    )


class Owner(Base):
    __tablename__ = 'owners'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    first = Column(String(255))
    last = Column(String(255))
    middle = Column(String(255))
    org_id = Column(Integer, ForeignKey('organizations.id'))
    organization = relationship(
        Organization, backref='owners', lazy='joined'
    )


class Search(Base):
    __tablename__ = 'search'
    __table_args__ = {'extend_existing': True}

    id = Column(
        UUIDType(binary=False),
        primary_key=True,
        unique=True,
        default=uuid.uuid4()
    )
    status = Column(
        Enum(SearchStatus), index=True
    )
    query = Column(String(255))
    date = Column(DateTime)
    dag_id = Column(String(255))
    dag_run_id = Column(String(255))
    meta_data = Column(JSON)
    user_id = Column(Integer)


__all__ = ['Requisite', 'Owner', 'Organization', 'Search']
