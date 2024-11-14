from typing import List, Optional, Type, TypeVar

from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.auth.models import User
from src.auth.schemas import RegisterUser
from src.notes.models import Note
from src.notes.schemas import NoteData

T = TypeVar('T')


class BaseDAO:
    model: Type[T] = None

    @classmethod
    async def get_all(cls, session: AsyncSession) -> List[T]:
        try:
            result = await session.execute(select(cls.model))
            return result.scalars().all()
        except Exception as ex:
            logger.error(f'Error in DAO get_all: {ex}')
            return []

    @classmethod
    async def get_one_or_none(cls, session: AsyncSession, **filters) -> Optional[T]:
        try:
            result = await session.execute(select(cls.model).filter_by(**filters))
            return result.scalar_one_or_none()
        except Exception as ex:
            logger.error(f'Error in DAO get_one: {ex}')
            return None

    @classmethod
    async def delete_by_id(cls, session: AsyncSession, **filters) -> Optional[T]:
        model_obj = await cls.get_one_or_none(session, **filters)
        if not model_obj:
            logger.warning(f"Object not found for deletion with filters: {filters}")
            return None

        try:
            await session.delete(model_obj)
            await session.commit()
            return model_obj
        except Exception as ex:
            logger.error(f'Error in delete_by_id: {ex}')
            await session.rollback()
            return None


class NoteDAO(BaseDAO):
    model = Note

    @classmethod
    async def create_note(cls, session: AsyncSession, note_data: NoteData) -> Optional[Note]:
        note = Note(owner_email=note_data.owner_email, title=note_data.title, text=note_data.text)
        try:
            session.add(note)
            await session.commit()
            logger.info(f'Created new note for user: {note_data.owner_email}')
            return note
        except IntegrityError as ex:
            logger.error(f"Integrity error in create_note: {ex}")
            await session.rollback()
            return None
        except Exception as ex:
            logger.error(f'Error in create_note: {ex}')
            await session.rollback()
            return None

    @classmethod
    async def get_all_notes_by_email(cls, session: AsyncSession, user_email: str) -> List[Note]:
        try:
            result = await session.execute(select(Note).where(Note.owner_email == user_email))
            logger.info(f'Retrieved all notes for: {user_email}')
            return result.scalars().all()
        except Exception as ex:
            logger.error(f'Error in get_all_notes_by_email: {ex}')
            return None


class UserDAO(BaseDAO):
    model = User

    @classmethod
    async def create_user(cls, session: AsyncSession, user_data: RegisterUser) -> Optional[User]:
        user = User(name=user_data.username, email=user_data.email)
        try:
            session.add(user)
            await session.commit()
            logger.info(f'Created new user: {user_data.email}')
            return user
        except IntegrityError as ex:
            logger.error(f"Integrity error in create_user: {ex}")
            await session.rollback()
            return None
        except Exception as ex:
            logger.error(f'Error in create_user: {ex}')
            await session.rollback()
            return None
