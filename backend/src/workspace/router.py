from typing import Annotated

from fastapi import APIRouter, Depends, Header
from fastapi.responses import Response
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.auth import authentication, get_payload_from_token, apikey_scheme
from src.auth.user import get_user_by_token, get_user_by_email
from src.db.database import get_async_session
from src.exceptions import AuthException
from src.workspace.models import Workspace, Invite
from src.workspace.schemas import WorkspaceCreate, WorkspaceRead, WorkspaceUpdate, WorkspaceInvite, InviteResolver
from src.workspace.workspace import create_new_workspace, get_workspace, update_workspace, invite_user, get_all_invites, \
    invite_resolver, get_all_workspaces, get_workspace_users

router = APIRouter()


@router.post('/invite')
async def invite_user_endpoint(
        request_body: WorkspaceInvite,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')

    return await invite_user(current_user, request_body, session)
    # result = await session.execute(select(Workspace).where(Workspace.id == workspace_id))
    # workspace = result.scalars().one()
    # inviter = await get_user_by_email(request_body.inviter, session)
    # if inviter is None:
    #     return Response(status_code=404, content='User not found')
    # invite = Invite(
    #     user_sender_id=current_user.id,
    #     user_inviter_id=inviter.id,
    #     target_workspace_id=workspace.id
    # )
    # session.add(invite)
    # return Response(status_code=200, content='OK')


@router.get('/invite')
async def get_all_invites_endpoint(
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')

    res = await get_all_invites(current_user, session)
    return res


@router.patch('/invite')
async def invite_resolver_endpoint(
        request_body: InviteResolver,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await invite_resolver(request_body, current_user, session)


@router.get('/all')
async def get_all_workspaces_endpoint(
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    """
    Получение всех рабочих пространств пользователя
    :param access_token:
    :param session:
    :return:
    """
    try:
        current_user = await get_user_by_token(access_token, session)
        return await get_all_workspaces(current_user, session)
    except:
        return Response(status_code=401, content='Unauthorized')


@router.get('/{workspace_id}/users')
async def get_workspace_users_endpoint(
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
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    return await get_workspace_users(workspace_id, current_user, session)


@router.post('/', status_code=201)
async def create_workspace(
        request_body: WorkspaceCreate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')
    create_data = request_body.model_dump()
    return await create_new_workspace(create_data, user, session)


@router.get('/{workspace_id}')
async def get_workspace_endpoint(
        workspace_id: int,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')

    current_workspace = await get_workspace(workspace_id, current_user, session)

    return current_workspace if current_workspace else Response(status_code=403, content='Forbidden')


@router.patch('/{workspace_id}')
async def update_workspace_endpoint(
        workspace_id: int,
        request_body: WorkspaceUpdate,
        access_token: Annotated[str, Depends(apikey_scheme)],
        session: AsyncSession = Depends(get_async_session),
):
    try:
        current_user = await get_user_by_token(access_token, session)
    except:
        return Response(status_code=401, content='Unauthorized')

    return await update_workspace(workspace_id, current_user, request_body, session)




# async def update_workspace_old_endpoint(
#         request_body: WorkspaceUpdate,
#         session: AsyncSession = Depends(get_async_session),
#         Authorization: str = Header()
# ):
#     update_data = request_body.model_dump()
#     workspace_id = update_data.pop('id')
#     stmt = update(Workspace).where(Workspace.id == workspace_id).values(**update_data).returning(Workspace)
#     result = await session.execute(stmt)
#     await session.commit()
#     return result
