from __future__ import annotations

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

from src.postgres_config.config import async_url


class Base(DeclarativeBase, AsyncAttrs):
    pass


engine = create_async_engine(async_url)
async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_async_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def cron_del():
    """
    Trigger for interval deletion rows in NOTE_SHARE_LINK_TABLE

    :return: NoReturn
    """
    with engine.connect() as conn:
        # Выполняем создание функции и триггера
        await conn.execute(text(
            ''' CREATE OR REPLACE FUNCTION delete_old_records() RETURNS TRIGGER AS $$ BEGIN DELETE FROM example WHERE created_at < NOW() - INTERVAL '10 minutes'; RETURN NULL; END; $$ LANGUAGE plpgsql; '''))

        await conn.execute(text(
            ''' CREATE TRIGGER delete_old_records_trigger AFTER INSERT ON example FOR EACH STATEMENT EXECUTE PROCEDURE delete_old_records(); '''))
