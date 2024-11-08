from sqlalchemy import URL

from src.config import settings


async_url = URL.create(
    drivername='postgresql+asyncpg',
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    database=settings.DB_NAME,
    username=settings.DB_USER,
    password=settings.DB_PASS
)
