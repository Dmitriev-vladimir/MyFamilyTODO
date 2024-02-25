from typing import Annotated

from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import apikey_scheme
from src.auth.user import get_user_by_token
from src.db.database import get_async_session
from src.project.project import create_new_project, update_project, get_all_projects
from src.project.schemas import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.post('/', status_code=201, response_model=None)
async def create_project_endpoint(
    request_body: ProjectCreate,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
) -> ProjectRead | Response:
    """
    Созадние проекта в Workspace
    :param request_body: словарь с данными проекта (модель ProjectCreate)
    :type request_body: ProjectCreate
    :param access_token: JWT токен доступа к API
    :type access_token: str
    :param session: объект сессии (Dependency Injection)
    :type session: AsyncSession
    :return: Объект созданного проекта (или Response) в случае неудачного создания
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    create_data = request_body.model_dump()
    return await create_new_project(create_data, user, session)


@router.post('/{project_id}', status_code=200)
async def update_project_endpoint(
    project_id: int,
    request_body: ProjectUpdate,
    access_token: Annotated[str, Depends(apikey_scheme)],
    session: AsyncSession = Depends(get_async_session),
):
    """
    Обновление данных о проекте
    :param project_id: id обновляемого проекта
    :type project_id: int
    :param request_body: словарь с обновляемыми данными (модель ProjectCreate)
    :type request_body: dict
    :param access_token: JWT токен доступа к API
    :type access_token: str
    :param session: объект сессии (Dependency Injection)
    :type session: AsyncSession
    :return: Response
    """
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    update_data = request_body.model_dump()
    res = await update_project(project_id, update_data, user, session)
    if res:
        return res
    return Response(status_code=404, content='Unexpected data')


@router.get('/{workspace_id}/all')
async def get_all_projects_endpoint(
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
    return await get_all_projects(workspace_id, user, session)
