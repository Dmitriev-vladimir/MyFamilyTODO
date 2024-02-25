from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import Response
from fastapi.responses import JSONResponse

from src.auth.auth import authentication, apikey_scheme, authenticate_user, get_payload_from_token, get_token
from src.auth.user import get_user_by_email, get_user_by_token, delete_user, update_user, get_all_users_in_workspace
from src.auth.models import User
from src.auth.schemas import UserCreate, UserLogin, UserUpdate, UserUpdateWorkspace
from src.auth.user import create_user
from src.db.database import get_async_session
from src.exceptions import AuthException
from src.workspace.models import UserWorkspace

router = APIRouter(prefix='/user', tags=['user'])


@router.post('/register', status_code=201)
async def register(request: UserCreate, session: AsyncSession = Depends(get_async_session)):
    """
    Метод регистрации пользователя в системе
    """
    create_data = request.model_dump()
    user = await create_user(create_data, session)
    access_token = get_token({
        'id': user.id,
        'role': str(user.role.value),
    })
    return JSONResponse(content=jsonable_encoder({'access_token': access_token}), status_code=201)


@router.post('/login')
async def login(
    request: UserLogin,
    session: AsyncSession = Depends(get_async_session),
):
    login_data = request.model_dump()
    user = await get_user_by_email(login_data.get('email'), session)

    if user is None:
        return Response(status_code=401, content='User does not exist')

    token_data = authenticate_user(user, login_data.get('password'))
    # TODO добавить refresh_token и после этого функцию обновления access token
    if token_data is None:
        return Response(status_code=401, content='Unauthorized')
    return token_data


@router.get('/all/{workspace_id}')
async def get_all_users(
    workspace_id: int,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session)
):
    # TODO Добавить выдачу данных только внутри своего workspace
    try:
        get_payload_from_token(access_token.replace('JWT ', ''))
    except AuthException:
        return Response(status_code=401, content='Unauthorized')

    return await get_all_users_in_workspace(workspace_id, session)


@router.get('/self')
async def get_user(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    return await get_user_by_token(access_token, session)


@router.delete('/self', status_code=204)
async def delete_self(
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session)
):
    return await delete_user(access_token, session)


@router.patch('/self', status_code=200)
async def update_self(
    request: UserUpdate,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    return await update_user(request, access_token, session)


@router.patch('/update/workspace', status_code=200)
@authentication
async def add_workspace(
    request: UserUpdateWorkspace,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Deprecated ???
    """
    update_data = request.model_dump()
    user_id = update_data.pop('id')
    for _id in update_data.get('workspaces'):
        stmt = insert(UserWorkspace).values({UserWorkspace.user_id: user_id, UserWorkspace.workspace_id: _id})
    #     stmt = update(User).where(User.id == user_id).values({User.workspace_id: _id}).returning(User)
        await session.execute(stmt)
        await session.commit()
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    return result.fetchone()[0]
