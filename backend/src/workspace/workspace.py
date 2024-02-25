from typing import Type, Optional

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import Response

from src.auth.schemas import UserRead
from src.auth.user import get_user_by_email
from src.workspace.models import Workspace, Invite, UserWorkspace
from src.auth.models import User
from src.workspace.schemas import WorkspaceRead, WorkspaceUpdate, WorkspaceInvite, InviteResolver


async def create_new_workspace(
    create_data: dict,
    user: Type[User],
    session: AsyncSession
) -> WorkspaceRead:
    workspace = Workspace(title=create_data.get('title'), admin=user.id)
    workspace.users = [user]
    workspace.admin = user.id
    session.add(workspace)
    await session.commit()
    res = WorkspaceRead(
        id=workspace.id,
        title=workspace.title,
        users=[el.id for el in workspace.users]
    )
    return res


async def get_workspace(
    workspace_id: int,
    current_user: Type[User],
    session: AsyncSession,
) -> Optional[WorkspaceRead]:
    query = select(Workspace).where(Workspace.id == workspace_id)
    # res = await session.get(query,)
    row_workspace = await session.execute(query)
    row_workspace = row_workspace.fetchone()
    workspace = row_workspace[0]
    # print('IN GET WORKSPACE:')
    # print(workspace.id)
    user_list = [el.id for el in workspace.users]
    # print('user list of workspace:', user_list)
    if current_user.id in user_list:
        return WorkspaceRead(
            id=workspace.id,
            title=workspace.title,
            users=[el.id for el in workspace.users]
        )
    return


async def update_workspace(
    workspace_id: int,
    current_user: Type[User],
    request_body: WorkspaceUpdate,
    session: AsyncSession,
) -> Response:
    query = select(Workspace).where(Workspace.id == workspace_id)
    row_workspace = (await session.execute(query)).fetchone()
    workspace = row_workspace[0]
    if current_user in workspace.users:
        workspace.title = request_body.new_title
        await session.commit()
        return Response(status_code=200, content='OK')
    return Response(status_code=403, content='Forbidden')


async def get_all_workspaces(
    current_user: Type[User],
    session: AsyncSession,
):
    # print('Start get all workspaces function')
    # print('User id in function get_all_workspaces:', current_user.id)
    query = select(Workspace).join(Workspace.users).where(User.id == current_user.id)
    # query = select(Workspace).join(Workspace.users).where(User.id == 2)
    # query = select(Workspace).filter(current_user in Workspace.users)
    # print(query)
    result_workspace = await session.execute(query)
    workspace_list = result_workspace.scalars().all()
    # print('workspace_list', workspace_list)
    # for ws in workspace_list:
    #     print('ws.id:', ws.id)
    #     for us in ws.users:
    #         print('us.id:', us.id)
    return [WorkspaceRead(
        id=el.id,
        title=el.title,
        users=[item.id for item in el.users]
    ) for el in workspace_list]


async def get_workspace_users(
    workspace_id: int,
    current_user: Type[User],
    session: AsyncSession,
):
    """

    :param workspace_id:
    :param current_user:
    :param session:
    :return:
    """
    current_user_workspaces = [el.id for el in await get_all_workspaces(current_user, session)]
    if workspace_id in current_user_workspaces:
        workspace = await session.get(Workspace, workspace_id)
        return [UserRead(
            id=user.id,
            username=user.username,
            telegram_name=user.telegram_name,
            email=user.email,
            role=user.role,
            registered_at=user.registered_at,
            is_active=user.is_active,
        ) for user in workspace.users]

    return Response(status_code=404, content='User not in workspace')

async def invite_user(
    current_user: Type[User],
    request_body: WorkspaceInvite,
    session: AsyncSession,
):
    workspace_id = request_body.workspace_id
    result = await session.execute(select(Workspace).where(Workspace.id == workspace_id))
    workspace = result.scalars().one()
    if workspace is None:
        return Response(status_code=404, content='Workspace not found')
    workspace_users = [el.id for el in workspace.users]
    if current_user.id not in workspace_users:
        return Response(status_code=404, content='User -sender not in target Workspace')
    inviter = await get_user_by_email(request_body.inviter, session)
    if inviter is None:
        return Response(status_code=404, content='User not found')
    invite = Invite(
        user_sender_id=current_user.id,
        user_inviter_id=inviter.id,
        target_workspace_id=workspace.id,
        status=True,
        result=None
    )
    session.add(invite)
    await session.commit()
    # print('INVITE:', invite.id, invite.target_workspace_id, invite.user_sender_id, invite.user_inviter_id)
    return Response(status_code=200, content='OK')


async def get_all_invites(
    current_user: Type[User],
    session: AsyncSession
):
    query_to = select(Invite).filter(and_(Invite.user_inviter_id == current_user.id, Invite.status == True))
    # query_to = select(Invite).where(Invite.user_inviter_id == current_user.id)

    result_to = await session.execute(query_to)
    invites_to = [el[0] for el in result_to.all()]

    query_from = select(Invite).filter(and_(Invite.user_sender_id == current_user.id, Invite.status is True))
    result_from = await session.execute(query_from)
    invites_from = [el[0] for el in result_from.all()]

    return {
        'to': invites_to,
        'from': invites_from
    }


async def invite_resolver(
    request_body: InviteResolver,
    current_user: Type[User],
    session: AsyncSession,
):
    query = select(Invite).where(Invite.id == request_body.id)
    invite_row = await session.execute(query)
    invite, *_ = invite_row.fetchone()
    if invite.user_inviter_id == current_user.id:
        invite.result = request_body.result
        invite.status = False
        session.add(invite)
        # print(
        #     'invite.id:', invite.id, 'invite.user_sender_id:', invite.user_sender_id, 'invite.user_inviter_id:',
        #     invite.user_inviter_id, 'invite.target_workspace_id:', invite.target_workspace_id)
        # print('current user:', current_user.id)
        await session.commit()
        # print('request_body.result:', request_body.result)
        if request_body.result:
            query = select(Workspace).where(Workspace.id == invite.target_workspace_id)
            workspace_row = await session.execute(query)
            workspace, *_ = workspace_row.one()
            # print('Finded workspace:', workspace.id)
            # print('Users before:', [el.id for el in workspace.users])
            workspace.users.append(current_user)
            # user_workspace = UserWorkspace(user_id=current_user.id, workspace_id=workspace.id)
            # print('New workspace', workspace)
            # print('Users after:', [el.id for el in workspace.users])
            # session.add_all([workspace, user_workspace])
            session.add(workspace)
            await session.commit()
            # print('Control users after commit:', [el.id for el in workspace.users])
            # print('user_workspace.id:', user_workspace.id)

        return Response(status_code=200, content='OK')
    return Response(status_code=403, content='Unforbidden')
