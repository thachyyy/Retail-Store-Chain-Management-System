from functools import lru_cache
from typing import Iterator

import sqlalchemy as sa
from fastapi_utils.session import FastAPISessionMaker as FastAPISessionMakerBase
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.settings import settings


class FastAPISessionMaker(FastAPISessionMakerBase):
    @staticmethod
    def _get_engine(uri: str) -> sa.engine.Engine:
        """
        Returns a sqlalchemy engine with pool_pre_ping enabled.

        This function may be updated over time to reflect recommended engine configuration for use with FastAPI.
        """
        return sa.create_engine(uri, poolclass=NullPool, convert_unicode=True,
                                echo=True if settings.SQLALCHEMY_DEBUG else False)

    def get_new_engine(self) -> sa.engine.Engine:
        """
        Returns a new sqlalchemy engine using the instance's database_uri.
        """
        return self._get_engine(self.database_uri)


@lru_cache()
def get_session_maker() -> FastAPISessionMaker:
    return FastAPISessionMaker(settings.SQLALCHEMY_DATABASE_URI)


def get_db() -> Iterator[Session]:
    """
    A generator function that yields an ORM session using the provided sessionmaker, and cleans it up when resumed.
    """
    engine = get_session_maker().get_new_engine()
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = session_local()

    try:
        yield session
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
