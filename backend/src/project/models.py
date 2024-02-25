from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class Project(Base):
    __tablename__ = 'project'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(length=240), nullable=False, unique=True, index=True)
    workspace: Mapped[int] = mapped_column(Integer, ForeignKey('workspace.id'))
