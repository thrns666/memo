import asyncio
import os
from typing import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy import NullPool, URL, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine, AsyncSession
from starlette.testclient import TestClient

from main import memo_app
from postgre_db.models import Base

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
Base.metadata.bind = engine_test


async def override_get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session


memo_app.dependency_overrides[async_session] = override_get_session


@pytest.fixture(autouse=True, scope='session')
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='session')
def even_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(memo_app)


@pytest.fixture(scope='session')
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=memo_app, base_url='http://test') as ac:
        yield ac
