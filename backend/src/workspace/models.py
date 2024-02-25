from typing import Optional, Set, List, Dict, Any

from pydantic import model_serializer
from sqlalchemy import Integer, String, ForeignKey, PrimaryKeyConstraint, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ARRAY

# from src.auth.models import User
from src.db.database import Base


class UserWorkspace(Base):
    __tablename__ = 'user_workspace'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    workspace_id: Mapped[int] = mapped_column(Integer, ForeignKey('workspace.id'))


class Invite(Base):
    __tablename__ = 'user_invite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_sender_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    user_inviter_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    target_workspace_id: Mapped[int] = mapped_column(Integer, ForeignKey('workspace.id'))
    status: Mapped[bool] = mapped_column(Boolean, default=True)
    result: Mapped[bool] = mapped_column(Boolean, nullable=True)


class Workspace(Base):
    __tablename__ = 'workspace'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=240), nullable=False, index=True)
    admin: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), default=1)

    users = relationship(
        'User', secondary='user_workspace', back_populates='workspaces', uselist=True, lazy="selectin")

    @model_serializer
    def ser_model(self) -> Dict[str, Any]:
        return {'id': self.id, 'title': self.title, 'users': [user.id for user in self.users]}
