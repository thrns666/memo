from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from src.auth.models import User
from src.postgres_config.database import Base


class Note(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    text: Mapped[str] = mapped_column(String(1000), default='')
    owner_email: Mapped[str] = mapped_column(ForeignKey('user.email'))
    owner: Mapped['User'] = relationship(back_populates='note', lazy='subquery')

    def __repr__(self):
        return f'{self.owner.name} -- {self.text}'
