import traceback
from typing import List
from sqlalchemy.future import select
from postgre_db.crud import async_session
from postgre_db.models import Note, User
from loguru import logger

from postgre_db.schemas import RegisterUser, NoteData


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

    @classmethod
    async def create_note(cls, note_data: NoteData):
        async with async_session() as session:
            try:
                note = Note(owner_id=note_data.name, text=note_data.text)
                session.add(note)
                await session.commit()

                logger.info(f'Created new note: {note_data.owner_id}')
            except Exception as ex:
                logger.error(f'Error in create_note: {ex}')

                return


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def create_user(cls, user_data: RegisterUser):
        async with async_session() as session:
            try:
                user = User(name=user_data.name, email=user_data.email)
                session.add(user)
                await session.commit()

                logger.info(f'Created new user: {user_data.email}')
            except Exception as ex:
                logger.error(f'Error in create_user: {ex}')

                return
