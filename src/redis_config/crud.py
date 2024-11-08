import traceback

from loguru import logger

from src.redis_config.config import connect_to_redis
from src.redis_config.schemas import RedisLoginData


async def get_session(email: str):
    redis_client = await connect_to_redis()
    try:
        result = await redis_client.get(email)

        if result:
            logger.info(f'Get session in redis: {result}')
            return result

        return None
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in redis get session: {ex}')
        return None
    finally:
        await redis_client.aclose()


async def put_session(data: RedisLoginData):
    redis_client = await connect_to_redis()
    try:
        await redis_client.set(data.email, data.user_password, ex=230)
        logger.info(f'Put session in redis: {data}')
        return True
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in redis put session: {ex}')
        return None
    finally:
        await redis_client.aclose()
