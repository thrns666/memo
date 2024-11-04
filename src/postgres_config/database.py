from __future__ import annotations
from dotenv import load_dotenv
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from config import settings

load_dotenv()

async_url = URL.create(
    drivername='postgresql+asyncpg',
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    username=settings.DB_USER,
    password=settings.DB_PASS
)


class Base(DeclarativeBase, AsyncAttrs):
    pass


engine = create_async_engine(async_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
