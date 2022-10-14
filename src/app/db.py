import logging
import os

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()

async_session = sessionmaker(
    engine, class_=AsyncSession, future=True, autoflush=False
)


async def db_session() -> AsyncSession:
    try:
        yield async_session
    except SQLAlchemyError as exc:
        logger.exception(exc)
