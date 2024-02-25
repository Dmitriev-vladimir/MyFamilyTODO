from typing import Optional

from pydantic import BaseModel


class Project(BaseModel):
    title: str
    workspace_id: int

    class ConfigDict:
        from_attributes = True


class ProjectCreate(Project):
    pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = ''
    workspace_id: Optional[int] = 0


class ProjectRead(Project):
    id: int
