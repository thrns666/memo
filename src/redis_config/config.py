import hashlib

import redis.asyncio as redis
from src.config import settings

redis_password_hash = hashlib.sha256(settings.REDIS_PASS.encode()).hexdigest()


async def connect_to_redis():
    return redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=0,
        username=settings.REDIS_USER,
        password=settings.REDIS_PASS
    )
