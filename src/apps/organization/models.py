from sqlalchemy import (
    Column, ForeignKey, Integer, String, Date, JSON, Enum
)
from sqlalchemy.orm import relationship

from src.apps.organization.schemas import OrganizationStatus
from src.core.database import Base


class Requisite(Base):
    __tablename__ = 'requisites'

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey('organizations.id'))
    type = Column(String, index=True)
    ogrn = Column(Integer)
    date = Column(Date, index=True)
    registrar = Column(String(255))
    address = Column(JSON)
    reg_number = Column(Integer)
    name = Column(String(255))
    category = Column(String(255))
    organization = relationship('Organization', back_populates='requisites')


class Owner(Base):
    __tablename__ = 'owner'

    id = Column(Integer, primary_key=True, index=True)
    org_id = Column(Integer, ForeignKey('organizations.id'))
    first = Column(String)
    last = Column(String)
    middle = Column(String)
    organization = relationship('Organization', back_populates='owner')


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, index=True)
    id_org = Column(Integer, unique=True, index=True)
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
    owner = relationship(Owner, back_populates='organization_owner')
    requisites = relationship(Requisite, back_populates='organization_reqs')


__all__ = ['Requisite', 'Owner', 'Organization']
