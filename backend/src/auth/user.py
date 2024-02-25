import datetime
from typing import Optional, Type

from fastapi import Depends
from pydantic import EmailStr
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import Hasher, get_payload_from_token
from src.auth.models import User
from src.auth.schemas import UserRead, UserUpdate
from src.db.database import get_async_session
from src.workspace.models import Workspace, UserWorkspace


async def create_user(create_data: dict, session: AsyncSession) -> UserRead:
    hashed_password = Hasher.get_password_hash(create_data.get('password'))

    create_data.pop('password')
    registered_at = datetime.datetime.utcnow()

    create_data.update({
        'registered_at': registered_at,
    })

    user = User(
        username=create_data.get('username'),
        hashed_password=hashed_password,
        telegram_name=create_data.get('telegram_name'),
        email=create_data.get('email'),
        role=create_data.get('role'),
        registered_at=registered_at,
        is_active=True,
    )
    # session.add(user)
    # await session.commit()
    workspace = Workspace(title=f'{create_data.get("username")}`s workspace')
    user.workspaces = [workspace]
    workspace.users = [user]

    session.add_all([user, workspace])

    await session.commit()
    workspace.admin = user.id

    await session.commit()
    return UserRead(
        id=user.id,
        username=create_data.get('username'),
        telegram_name=create_data.get('telegram_name'),
        email=create_data.get('email'),
        role=create_data.get('role'),
        registered_at=registered_at,
        is_active=True,
        workspaces=[item.ser_model() for item in user.workspaces]
    )


async def get_user_by_email(email: EmailStr, session: AsyncSession) -> Optional[User]:
    query = select(User).where(User.email == email)
    result = await session.execute(query)
    row_user = result.fetchone()
    if row_user:
        return row_user[0]
    return None


async def get_user_by_id(user_id: int, session: AsyncSession) -> Optional[Type[User]]:
    user = await session.get(User, user_id)
    if user:
        return user
    return None


async def get_user_by_token(access_token: str, session: AsyncSession) -> Optional[Type[User]]:
    payload = get_payload_from_token(access_token.replace('JWT ', ''))
    user = await session.get(User, payload.get('id'))

    if user:
        return user
    return None


async def delete_user(access_token: str, session: AsyncSession) -> Optional[int]:
    user = await get_user_by_token(access_token, session)
    if user:
        stmt = update(User).where(User.id == user.id).values(is_active=False)
        await session.execute(stmt)
        await session.commit()
        return user.id
    return None


async def update_user(
    user_data: UserUpdate,
    access_token: str,
    session: AsyncSession
):
    update_data = user_data.model_dump(exclude_unset=True)
    user = await get_user_by_token(access_token, session)
    if update_data.get('password'):
        password = update_data.pop('password')
        update_data.update({'hashed_password': Hasher.get_password_hash(password)})

    stmt = update(User).where(User.id == user.id).values(update_data).returning(User)
    result = await session.execute(stmt)
    await session.commit()
    upd_user, *_ = result.fetchone()
    return upd_user


async def get_all_users_in_workspace(
    workspace_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    query = select(User).order_by(User.id).filter(User.workspaces.any(UserWorkspace.workspace_id == workspace_id))
    users = await session.execute(query)
    result = [item[0] for item in users.all()]
    return result
