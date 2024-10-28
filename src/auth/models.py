from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.postgres_config.database import Base


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    notes: Mapped[List['Note']] = relationship(back_populates='owner', cascade='all, delete-orphan', lazy='subquery')

    def __repr__(self):
        return f'{self.name} ** {self.id}'
