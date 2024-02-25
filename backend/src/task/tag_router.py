from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import apikey_scheme
from src.auth.user import get_user_by_token
from src.db.database import get_async_session
from src.task.schemas import TagCreate, TagUpdate
from src.task.tag import create_tag, update_tag, get_all_tags

router = APIRouter()


@router.post('/', status_code=201)
async def create_tag_endpoint(
        create_data: TagCreate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await create_tag(create_data, user, session)


@router.patch('/', status_code=200)
async def update_tag_endpoint(
        update_data: TagUpdate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await update_tag(update_data, user, session)


@router.get('/all/{workspace_id}')
async def get_all_tags_endpoint(
        workspace_id: int,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    """

    :param workspace_id:
    :param access_token:
    :param session:
    :return:
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await get_all_tags(workspace_id, user, session)
