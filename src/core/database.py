from typing import Iterator

from async_lru import alru_cache
from fastapi_utils.session import FastAPISessionMaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

from settings import Configuration

SQLALCHEMY_DATABASE_URL = 'sqlite:///./sql_app.db'

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


@alru_cache(maxsize=32)
def _get_fastapi_sessionmaker() -> FastAPISessionMaker:
    """ This function could be replaced with a global variable if preferred """
    database_uri = Configuration().DATABASE_URI
    return FastAPISessionMaker(database_uri)


def get_db_instance() -> Iterator[Session]:
    """ FastAPI dependency that provides a sqlalchemy session """
    yield from _get_fastapi_sessionmaker().get_db()
