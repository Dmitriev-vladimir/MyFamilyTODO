from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import apikey_scheme
from src.auth.user import get_user_by_token
from src.db.database import get_async_session
from src.task.color import create_color, get_color, get_all_colors, update_color
from src.task.schemas import ColorCreate, ColorUpdate

router = APIRouter()


@router.post('/', status_code=201)
async def create_color_endpoint(
        create_data: ColorCreate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await create_color(create_data, user, session)


@router.patch('/', status_code=200)
async def create_color_endpoint(
        update_data: ColorUpdate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    """

    :param update_data:
    :param access_token:
    :param session:
    :return:
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await update_color(update_data, user, session)


@router.get('/all/{workspace_id}')
async def get_all_colors_endpoint(
        workspace_id: int,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')

    return await get_all_colors(workspace_id, user, session)


@router.get('/{color_id}')
async def get_color_endpoint(
        color_id: int,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await get_color(color_id, user, session)
