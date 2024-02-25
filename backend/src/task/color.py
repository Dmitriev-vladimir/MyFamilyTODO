from typing import Type
from fastapi import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.task.models import Color
from src.task.schemas import ColorCreate, ColorRead, ColorUpdate
from src.workspace.models import Workspace, UserWorkspace
from src.workspace.workspace import get_all_workspaces


async def create_color(
        create_data: ColorCreate,
        current_user: Type[User],
        session: AsyncSession
):
    """
    Создание цвета
    :param create_data:
    :param current_user:
    :param session:
    :return:
    """
    current_user_workspaces = [el.id for el in await get_all_workspaces(current_user, session)]

    if create_data.workspace_id in current_user_workspaces:
        color = Color(
            name=create_data.name,
            value=create_data.value,
            workspace_id=create_data.workspace_id
        )
        session.add(color)
        await session.commit()
        result = ColorRead(
            id=color.id,
            name=color.name,
            value=color.value,
            workspace_id=color.workspace_id
        )
        return result
    return Response(status_code=404, content='User not in workspace')


async def update_color(
        update_data: ColorUpdate,
        current_user: Type[User],
        session: AsyncSession
):
    """

    :param update_data:
    :param current_user:
    :param session:
    :return:
    """
    color = await session.get(Color, update_data.id)
    current_user_workspaces = [el.id for el in await get_all_workspaces(current_user, session)]

    if color.workspace_id in current_user_workspaces:
        if update_data.name:
            color.name = update_data.name
        if update_data.value:
            color.value = update_data.value
        session.add(color)
        await session.commit()
        return ColorRead(
            id=color.id,
            name=color.name,
            value=color.value,
            workspace_id=color.workspace_id
        )
    return Response(status_code=404, content='User not in color workspace')


async def get_color(
        color_id: int,
        current_user: Type[User],
        session: AsyncSession
):
    query = select(Color).where(Color.id == color_id)

    result = await session.execute(query)
    result_color, *_ = result.one()
    return ColorRead(
        id=result_color.id,
        name=result_color.name,
        value=result_color.value,
        workspace_id=result_color.workspace_id
    )


async def get_all_colors(
        workspace_id: int,
        user: Type[User],
        session: AsyncSession
):
    # query = select(Workspace).where(UserWorkspace.user_id == user.id)
    #
    # result_workspace = await session.execute(query)
    # workspace_list, *_ = result_workspace.all()
    current_user_workspaces = [el.id for el in await get_all_workspaces(user, session)]
    if workspace_id in current_user_workspaces:
        color_query = select(Color).where(Color.workspace_id == workspace_id)
        result_colors = await session.execute(color_query)
        color_list = result_colors.all()
        return [ColorRead(
            id=el[0].id,
            workspace_id=el[0].workspace_id,
            name=el[0].name,
            value=el[0].value
        ) for el in color_list]
    return Response(status_code=404, content='Not valid workspace')
