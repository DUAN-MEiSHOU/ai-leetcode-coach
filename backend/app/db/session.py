from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings


def create_session_factory(database_url: str) -> sessionmaker[Session]:
    engine = create_engine(database_url, pool_pre_ping=True)
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


def get_session() -> Generator[Session, None, None]:
    session = create_session_factory(get_settings().database_url)()
    try:
        yield session
    finally:
        session.close()
