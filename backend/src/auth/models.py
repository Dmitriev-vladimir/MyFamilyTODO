import enum
from datetime import datetime

from sqlalchemy import Integer, String, TIMESTAMP, Boolean, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class UserRole(enum.Enum):
    owner = 'owner'
    admin = 'admin'
    user = 'user'


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    telegram_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
    registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    workspaces = relationship('Workspace', secondary='user_workspace', back_populates='users', uselist=True)
