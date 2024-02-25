import enum
from typing import Optional, Set

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class Task(Base):
    __tablename__ = 'task'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=240), nullable=False, unique=True, index=True)

    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'), nullable=True)
    project_id: Mapped[int] = mapped_column(ForeignKey('project.id'), nullable=True)
    tags: Mapped[Optional[Set['Tag']]] = relationship()
    tag_id: Mapped[Optional[Set[int]]] = mapped_column(ForeignKey('tag.id'), nullable=True)

    colors: Mapped[Optional[Set['Tag']]] = relationship()
    color_id: Mapped[Optional[Set[int]]] = mapped_column(ForeignKey('color.id'), nullable=True)
    executor: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'), nullable=True)
    status: Mapped[str] = mapped_column(String, default='active', nullable=True)


class Tag(Base):
    __tablename__ = 'tag'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'), nullable=True)


class Color(Base):
    __tablename__ = 'color'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    value: Mapped[str] = mapped_column(String, nullable=False)
    workspace_id: Mapped[int] = mapped_column(ForeignKey('workspace.id'), nullable=True)

