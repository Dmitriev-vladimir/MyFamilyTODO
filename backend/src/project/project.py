from typing import Type

from fastapi import Response

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.project.models import Project
from src.project.schemas import ProjectCreate, ProjectRead
from src.workspace.models import Workspace, UserWorkspace
from src.workspace.workspace import get_all_workspaces


async def create_new_project(
    create_data: dict,
    user: Type[User],
    session: AsyncSession
):
    """
    Функция создания проекта
    :param create_data: данные создаваемого проекта
    :type create_data: dict
    :param user: текущий пользователь
    :type user: User
    :param session: объект сессии (Dependency Injection)
    :type session: AsyncSession
    :return: объект ProjectRead
    """
    project = Project(title=create_data.get('title'), workspace=create_data.get('workspace_id'))
    session.add(project)
    await session.commit()
    return ProjectRead(
        id=project.id,
        title=project.title,
        workspace_id=project.workspace
    )


async def update_project(
        project_id: int,
        update_data: dict,
        user: Type[User],
        session: AsyncSession
) -> ProjectRead:
    """
    Функция создания проекта
    :param project_id: id обновляемого проекта
    :type project_id: int
    :param update_data: обновляемые данные проекта
    :type update_data: dict
    :param user: текущий пользователь
    :type user: User
    :param session: объект сессии (Dependency Injection)
    :type session: AsyncSession
    :return: объект ProjectRead
    """
    query = select(Project).where(Project.id == project_id)
    row_project = await session.execute(query)
    project = row_project.fetchone()[0]
    query_workspace = select(Workspace).filter(Workspace.users.any(UserWorkspace.user_id == user.id))
    row_workspaces = await session.execute(query_workspace)
    workspaces = [el[0] for el in row_workspaces.all()]
    workspace_ids = [el.id for el in workspaces]
    if project.workspace in workspace_ids:
        admin_id_list = [el.admin for el in workspaces if el.id == project.workspace]
        if len(admin_id_list) == 1:
            if admin_id_list[0] == user.id:
                workspace_id = update_data.pop('workspace_id')
                title = update_data.pop('title')
                if workspace_id != 0 and workspace_id in workspace_ids:
                    update_data.update({
                        'workspace': workspace_id
                    })
                if title != '':
                    update_data.update({
                        'title': title
                    })
                stmt = update(Project).where(Project.id == project_id).values(update_data).returning(Project)
                result = await session.execute(stmt)
                await session.commit()
                upd_project, *_ = result.fetchone()
                return upd_project


async def get_all_projects(
        workspace_id: int,
        user: Type[User],
        session: AsyncSession
):
    """

    :param workspace_id:
    :param user:
    :param session:
    :return:
    """
    current_user_workspaces = [el.id for el in await get_all_workspaces(user, session)]

    if workspace_id in current_user_workspaces:
        query = select(Project).where(Project.workspace == workspace_id)
        row = await session.execute(query)
        return [ProjectRead(
            id=project[0].id,
            title=project[0].title,
            workspace_id=project[0].workspace
        ) for project in row.all()]
    return Response(status_code=404, content='User not in tag workspace')