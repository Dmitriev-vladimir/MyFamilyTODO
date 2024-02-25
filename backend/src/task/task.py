import copy
from typing import Type

from fastapi import Response

from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.project.models import Project
from src.task.models import Task
from src.task.schemas import TaskCreate, TaskRead, TaskUpdate
from src.workspace.workspace import get_all_workspaces


async def create_new_task(
        create_data: TaskCreate,
        user: Type[User],
        session: AsyncSession
):
    task = Task(
        title=create_data.title,
        project_id=create_data.project_id,
        workspace_id=create_data.workspace_id,
        color_id=create_data.color_id,
        tag_id=create_data.tag_id,
        executor=create_data.executor,
        status='active'
    )

    session.add(task)
    await session.commit()

    return TaskRead(
        id=task.id,
        title=task.title,
        project_id=task.project_id,
        workspace_id=task.workspace_id,
        color_id=task.color_id,
        tag_id=task.tag_id,
        executor=task.executor,
        status=task.status
    )


async def update_task(
        update_data: TaskUpdate,
        user: Type[User],
        session: AsyncSession
):
    update_dict = update_data.model_dump()
    control_dict = copy.deepcopy(update_dict)
    # if update_dict.get('status') and update_dict.get('status') not in ['active', 'done', 'deleted']:
    #     return Response(status_code=404, content='Not valid status')

    for key in control_dict.keys():
        if update_dict[key] is None:
            update_dict.pop(key)
    task_id = update_dict.pop('id')
    stmt = update(Task).where(Task.id == task_id).values(update_dict).returning(Task)
    result_row = await session.execute(stmt)
    result, *_ = result_row.fetchone()
    await session.commit()
    return TaskRead(
        id=result.id,
        title=result.title,
        project_id=result.project_id,
        workspace_id=result.workspace_id,
        color_id=result.color_id,
        tag_id=result.tag_id,
        executor=result.executor,
        status=result.status
    )


async def get_project_tasks(
        project_id: int,
        user: Type[User],
        session: AsyncSession
):
    current_user_workspaces = [el.id for el in await get_all_workspaces(user, session)]
    project = await session.get(Project, project_id)
    if project.workspace in current_user_workspaces:
        query = select(Task).where(Task.project_id == project_id)
        row = await session.execute(query)
        return [TaskRead(
            id=task[0].id,
            title=task[0].title,
            project_id=task[0].project_id,
            workspace_id=task[0].workspace_id,
            color_id=task[0].color_id,
            tag_id=task[0].tag_id,
            executor=task[0].executor,
            status=task[0].status
        ) for task in row.all()]
    return Response(status_code=404, content='Not valid project')


async def get_workspace_tasks(
        workspace_id: int,
        user: Type[User],
        session: AsyncSession
):
    current_user_workspaces = [el.id for el in await get_all_workspaces(user, session)]
    if workspace_id in current_user_workspaces:
        query = select(Task).where(Task.workspace_id == workspace_id)
        row = await session.execute(query)
        return [TaskRead(
            id=task[0].id,
            title=task[0].title,
            project_id=task[0].project_id,
            workspace_id=task[0].workspace_id,
            color_id=task[0].color_id,
            tag_id=task[0].tag_id,
            executor=task[0].executor,
            status=task[0].status
        ) for task in row.all()]
    return Response(status_code=404, content='Not valid workspace')
