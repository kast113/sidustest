from typing import Generator
import os

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import Base, db_session


DATABASE_URL = os.getenv("DATABASE_URL").replace('+asyncpg', '')
DATABASE_URL_TEST = os.getenv("DATABASE_URL").replace(
    '@db/postgres', '@db/test')



# @pytest.fixture
@pytest_asyncio.fixture
async def ac() -> Generator:
    async with AsyncClient(app=app, base_url="https://test") as c:
        os.environ["IS_TESTING"] = "True"
        yield c


@pytest.fixture(scope="session")
def setup_db() -> Generator:
    engine = create_engine(DATABASE_URL)
    conn = engine.connect()

    conn.execute("commit")
    try:
        conn.execute("drop database test")
    except SQLAlchemyError:
        pass
    finally:
        conn.close()

    conn = engine.connect()

    conn.execute("commit")
    conn.execute("create database test")
    conn.close()

    yield

    conn = engine.connect()

    conn.execute("commit")
    try:
        conn.execute("drop database test")
    except SQLAlchemyError:
        pass
    conn.close()


@pytest.fixture(scope="session", autouse=True)
def setup_test_db(setup_db):
    '''
    Recreate new test db for all session with migrations ??
    '''
    engine = create_engine(DATABASE_URL_TEST.replace('+asyncpg', ''))

    with engine.begin():
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        yield
        Base.metadata.drop_all(engine)



@pytest_asyncio.fixture
# @pytest.fixture
async def session():
    # https://github.com/sqlalchemy/sqlalchemy/issues/5811#issuecomment-756269881
    async_engine = create_async_engine(DATABASE_URL_TEST)
    async with async_engine.connect() as conn:

        await conn.begin()
        await conn.begin_nested()
        AsyncSessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=conn,
            future=True,
            class_=AsyncSession,
        )

        async_session = AsyncSessionLocal()

        @event.listens_for(async_session.sync_session, "after_transaction_end")
        def end_savepoint(session, transaction):
            if conn.closed:
                return
            if not conn.in_nested_transaction:
                conn.sync_connection.begin_nested()

        def test_db_session() -> Generator:
            try:
                yield AsyncSessionLocal
            except SQLAlchemyError as exc:
                print(exc)
                pass

        app.dependency_overrides[db_session] = test_db_session

        yield async_session
        await async_session.close()
        await conn.rollback()
