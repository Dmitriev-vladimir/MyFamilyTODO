from typing import List, Optional

from pydantic import BaseModel


class Workspace(BaseModel):
    title: str

    class ConfigDict:
        from_attributes = True


class WorkspaceCreate(Workspace):
    pass


class WorkspaceRead(Workspace):
    id: int
    users: List
    pass


class WorkspaceInvite(BaseModel):
    inviter: str
    workspace_id: int


class InviteResolver(BaseModel):
    id: int
    result: bool


class WorkspaceUpdate(BaseModel):
    new_title: Optional[str]
