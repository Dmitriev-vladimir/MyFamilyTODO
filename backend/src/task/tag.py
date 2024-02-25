from typing import Type

from fastapi import Response

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.models import User
from src.task.models import Tag
from src.task.schemas import TagCreate, TagRead, TagUpdate
from src.workspace.workspace import get_all_workspaces


async def create_tag(
        create_data: TagCreate,
        current_user: Type[User],
        session: AsyncSession
):
    """

    :param create_data:
    :param current_user:
    :param session:
    :return:
    """
    tag = Tag(
        name=create_data.name,
        workspace_id=create_data.workspace_id
    )
    session.add(tag)
    await session.commit()
    result = TagRead(
        id=tag.id,
        name=tag.name,
        workspace_id=tag.workspace_id
    )
    return result


async def update_tag(
        update_data: TagUpdate,
        current_user: Type[User],
        session: AsyncSession
):
    """

    :param update_data:
    :param current_user:
    :param session:
    :return:
    """
    tag = await session.get(Tag, update_data.id)
    current_user_workspaces = [el.id for el in await get_all_workspaces(current_user, session)]

    if tag.workspace_id in current_user_workspaces:
        tag.name = update_data.name
        session.add(tag)
        await session.commit()
        return TagRead(
            id=tag.id,
            name=tag.name,
            workspace_id=tag.workspace_id
        )
    return Response(status_code=404, content='User not in tag workspace')


async def get_all_tags(
        workspace_id: int,
        current_user: Type[User],
        session: AsyncSession
):
    """

    :param workspace_id:
    :param current_user:
    :param session:
    :return:
    """
    current_user_workspaces = [el.id for el in await get_all_workspaces(current_user, session)]

    if workspace_id in current_user_workspaces:
        query = select(Tag).where(Tag.workspace_id == workspace_id)
        row = await session.execute(query)
        tag_list = [TagRead(
            id=el[0].id,
            name=el[0].name,
            workspace_id=el[0].workspace_id
        ) for el in row.all()]
        return tag_list
    return Response(status_code=404, content='User not in tag workspace')
