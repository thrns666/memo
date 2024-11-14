import asyncio
import os
from typing import AsyncGenerator
import pytest
from dotenv import load_dotenv
from sqlalchemy import NullPool, URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from starlette.testclient import TestClient
from auth.utils import get_user_from_token
from src.main import memo_app
from src.postgres_config.database import Base, get_async_session

load_dotenv()

DATABASE_URL_TEST = URL.create(
    drivername='postgresql+asyncpg',
    host=os.environ.get('DB_HOST_TEST'),
    port=os.environ.get('DB_PORT_TEST'),
    database=os.environ.get('DB_NAME_TEST'),
    username=os.environ.get('DB_USER_TEST'),
    password=os.environ.get('DB_PASS_TEST')
)

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session = async_sessionmaker(engine_test, expire_on_commit=False)


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


def override_get_user_from_token():
    return {'email': 'test@email.com'}


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def ac():
    memo_app.dependency_overrides.update(
        {
            get_async_session: override_get_async_session,
            get_user_from_token: override_get_user_from_token
         }
    )

    return TestClient(memo_app)


@pytest.fixture(scope='session')
async def session():
    async with async_session() as session:
        yield session
