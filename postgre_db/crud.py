from __future__ import annotations
import os
from typing import List, Sequence
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from postgre_db.models import User, Note, Base
from loguru import logger

load_dotenv()

async_url = URL.create(
    drivername='postgresql+asyncpg',
    host=os.environ.get('DB_HOST'),
    port=os.environ.get('DB_PORT'),
    database=os.environ.get('DB_NAME'),
    username=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASS')
)

# sync_url = URL.create(
#     drivername='postgresql+psycopg2',
#     host=os.environ.get('DB_HOST'),
#     port=os.environ.get('DB_PORT'),
#     database=os.environ.get('DB_NAME'),
#     username=os.environ.get('DB_USER'),
#     password=os.environ.get('DB_PASS')
# )

engine = create_async_engine(async_url)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# s_engine = create_engine(sync_url)
# Base.metadata.create_all(bind=s_engine)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


async def get_all_notes(session: AsyncSession) -> Sequence[Note]:
    result = await session.execute(select(Note))
    return result.scalars().all()


async def get_notes_by_user(session: AsyncSession, user_id: int):
    user_notes = await session.execute(select(Note).where(Note.owner_id == user_id))
    return user_notes.scalars().all()


async def create_note(session: AsyncSession, note: Note):
    session.add(note)
    await session.commit()
    logger.info(f'Create new note by: {note.owner}')
    return Note


async def create_user(name: str, email: str, session: AsyncSession) -> User | None:
    try:
        new_user = User(name=name, email=email)
        session.add(new_user)
        await session.commit()

        return new_user
    except Exception as ex:
        await session.rollback()
        logger.error(f'Error in create_user: {ex}')

        return None


async def get_user(user_id: int, session: AsyncSession) -> User | None:
    user = await session.execute(select(User).where(User.owner_id == user_id))
    return user.scalar_one_or_none()
