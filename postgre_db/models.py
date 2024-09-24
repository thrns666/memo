from typing import List
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'auth_users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    notes: Mapped[List['Note']] = relationship(back_populates='user', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.name} ** {self.id}'


class Note(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(1000), default='')
    owner_id: Mapped[int] = mapped_column(ForeignKey('auth_users.id'))
    owner: Mapped['User'] = relationship(back_populates='notes')

    def __repr__(self):
        return f'{self.owner.name} -- {self.text}'
