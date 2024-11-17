import asyncio
import datetime
from typing import AsyncGenerator

import pytest
from sqlalchemy import NullPool, URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from starlette.testclient import TestClient

from auth.utils import create_jwt_token
from config import settings
from src.main import memo_app
from src.postgres_config.database import Base

DATABASE_URL_TEST = URL.create(
    drivername='postgresql+asyncpg',
    host=settings.DB_HOST_TEST,
    port=settings.DB_PORT_TEST,
    database=settings.DB_NAME_TEST,
    username=settings.DB_USER_TEST,
    password=settings.DB_PASS_TEST
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


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def client():
    return TestClient(memo_app)


@pytest.fixture(scope='session')
async def session():
    async with async_session() as session:
        yield session


@pytest.fixture()
def jwt_login():
    token_data = {
        'sub': {
            'email': 'test@email.com',
        },
        'exp': datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=3000)
    }
    auth_token = create_jwt_token(token_data)
    return auth_token
