import traceback
import redis.asyncio as redis
from loguru import logger
from redis_config.models import RedisLoginData


async def connect_to_redis():
    return await redis.Redis(host='localhost', port=6379, db=0)


async def get_session(email: str):
    redis_client = await connect_to_redis()
    try:
        result = await redis_client.get(email)

        if result:
            logger.info(f'Get session in redis: {result}')
            print(result)
            return result

        return None
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in redis get session: {ex}')
        return None
    finally:
        await redis_client.close()


async def put_session(data: RedisLoginData):
    redis_client = await connect_to_redis()
    try:
        await redis_client.set(data.email, data.user_password)
        logger.info(f'Put session in redis: {data}')
        return True
    except Exception as ex:
        tb = traceback.format_exc()
        logger.error(f'Error in redis put session: {ex}')
        return None
    finally:
        await redis_client.close()
