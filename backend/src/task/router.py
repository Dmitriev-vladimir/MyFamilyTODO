from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import apikey_scheme
from src.auth.user import get_user_by_token
from src.db.database import get_async_session
from src.task.schemas import TaskCreate, TaskUpdate
from src.task.task import create_new_task, update_task, get_project_tasks, get_workspace_tasks

router = APIRouter()


@router.post('/', status_code=201)
async def create_task_endpoint(
    create_data: TaskCreate,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Создание задачи в проекте
    :param create_data:
    :param access_token:
    :param session:
    :return:
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await create_new_task(create_data, user, session)


@router.patch('/', status_code=200)
async def update_task_endpoint(
    update_data: TaskUpdate,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление задачи
    :param update_data:
    :param access_token:
    :param session:
    :return:
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await update_task(update_data, user, session)


@router.get('/project/{project_id}/all')
async def get_project_tasks_endpoint(
    project_id: int,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await get_project_tasks(project_id, user, session)


@router.get('/workspace/{workspace_id}/all')
async def get_workspace_tasks_endpoint(
    workspace_id: int,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await get_workspace_tasks(workspace_id, user, session)