from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    notes: Mapped[List['Note']] = relationship(back_populates='owner', cascade='all, delete-orphan', lazy='subquery')

    def __repr__(self):
        return f'{self.name} ** {self.id}'


class Note(Base):
    __tablename__ = 'note_table'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    text: Mapped[str] = mapped_column(String(1000), default='')
    owner_email: Mapped[str] = mapped_column(ForeignKey('user.email'))
    owner: Mapped['User'] = relationship(back_populates='notes', lazy='subquery')

    def __repr__(self):
        return f'{self.owner.name} -- {self.text}'
