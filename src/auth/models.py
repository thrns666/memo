from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.notes.models import Note
from src.postgres_config.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    registered_date: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    notes: Mapped[List['Note']] = relationship(back_populates='owner', cascade='all, delete-orphan', lazy='subquery')

    def __repr__(self):
        return f'{self.name} ** {self.id}'
