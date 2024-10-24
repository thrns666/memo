from __future__ import annotations
import os
from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

load_dotenv()

async_url = URL.create(
    drivername='postgresql+asyncpg',
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
    database=os.environ.get('DB_NAME'),
    username=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS')
)

engine = create_async_engine(async_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
