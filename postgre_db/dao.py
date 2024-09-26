import traceback
from typing import List
from sqlalchemy.future import select
from postgre_db.crud import async_session
from postgre_db.models import Note, User
from loguru import logger


class BaseDAO:
    model = None

    @classmethod
    async def get_all(cls) -> List[model]:
        async with async_session() as session:
            result = await session.execute(select(cls.model))
            return result.scalars().all()

    @classmethod
    async def get_one_or_none(cls, **filters) -> model:
        async with async_session() as session:
            try:
                result = await session.execute(select(cls.model).filter_by(**filters))
                return result.scalar_one_or_none()
            except Exception as ex:
                # tb = traceback.format_exc()
                logger.error(f'Error in DAO get_one: {ex}')

    @classmethod
    async def delete_by_id(cls, **filters):
        async with async_session() as session:
            model_obj = await cls.get_one_or_none(**filters)

            try:
                session.delete(model_obj)
                await session.commit()
            except Exception as ex:
                logger.error(f'Error in delete_by_id: {ex}')
                await session.rollback()


class NoteDAO(BaseDAO):
    model = Note


class UserDAO(BaseDAO):
    model = User
