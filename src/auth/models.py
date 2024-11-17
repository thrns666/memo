from datetime import datetime
from sqlalchemy import String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from src.postgres_config.database import Base


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str] = mapped_column(String(30), unique=True)
    registered_date: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f'{self.name} ** {self.id}'
