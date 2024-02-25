from typing import AsyncGenerator, Any

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import DeclarativeBase, declarative_base

from src.settings import settings

DATABASE_URL = settings.database_url

engine = create_async_engine(DATABASE_URL, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)


Base = declarative_base()
# @as_declarative()
# class Base:
#     id: Any
#     __name__: str
#
#     # Generate __tablename__ automatically
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
