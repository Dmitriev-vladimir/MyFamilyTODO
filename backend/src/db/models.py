# import enum
# from datetime import datetime
# from typing import Optional, Set
#
# from sqlalchemy import Integer, String, Enum, TIMESTAMP, Boolean, ForeignKey
# from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, declarative_base
#
# # class Base(DeclarativeBase):
# #     pass
#
#
#
# class UserRole(enum.Enum):
#     owner = 'owner'
#     admin = 'admin'
#     user = 'user'
#
#
# class User(Base):
#     __tablename__ = 'user'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     username: Mapped[str] = mapped_column(String, nullable=False)
#     hashed_password: Mapped[str] = mapped_column(String, nullable=False)
#     telegram_name: Mapped[str] = mapped_column(String, nullable=False)
#     email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
#     role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.user)
#     registered_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.utcnow)
#     is_active: Mapped[bool] = mapped_column(Boolean, default=True)
#
#
# class Workspace(Base):
#     __tablename__ = 'workspace'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(length=240), nullable=False, unique=True, index=True)
#
#
# class Project(Base):
#     __tablename__ = 'project'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(length=240), nullable=False, unique=True, index=True)
#     workspace: Mapped[int] = mapped_column(Integer, ForeignKey('workspace.id'))
#
#
# class Task(Base):
#     __tablename__ = 'task'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     title: Mapped[str] = mapped_column(String(length=240), nullable=False, unique=True, index=True)
#
#     project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))
#     tags: Mapped[Optional[Set['Tag']]] = relationship()
#     tag_id: Mapped[Optional[Set[int]]] = mapped_column(ForeignKey('tag.id'))
#
#     colors: Mapped[Optional[Set['Tag']]] = relationship()
#     color_id: Mapped[Optional[Set[int]]] = mapped_column(ForeignKey('color.id'))
#     executor: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
#
#
# class Tag(Base):
#     __tablename__ = 'tag'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#
#
# class Color(Base):
#     __tablename__ = 'color'
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     name: Mapped[str] = mapped_column(String, nullable=False)
#     value: Mapped[str] = mapped_column(String, nullable=False)
