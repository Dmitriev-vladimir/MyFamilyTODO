from typing import Optional, List

from pydantic import BaseModel, field_validator, root_validator, validator, model_validator


class Task(BaseModel):
    title: str
    workspace_id: Optional[int] = None
    project_id: Optional[int] = None
    color_id: int
    tag_id: int
    executor: int
    status: str

    @field_validator('status')
    @classmethod
    def control_status_choice(cls, status_val: str) -> str:
        if status_val.lower() not in ['active', 'done', 'deleted']:
            raise ValueError('Not valid Status value')
        return status_val.title()


class TaskCreate(Task):
    color_id: Optional[int] = None
    tag_id: Optional[int] = None
    executor: Optional[int] = None
    status: str = 'active'

    @model_validator(mode='before')
    @classmethod
    def control_task_ownership(cls, val):
        if val.get('project_id') is None and val.get('workspace_id') is None:
            raise ValueError('Not valid ownership')
        return val


class TaskRead(Task):
    id: int
    color_id: Optional[int] = None
    tag_id: Optional[int] = None
    executor: Optional[int] = None
    status: str


class TaskUpdate(Task):
    id: int
    title: Optional[str] = None
    color_id: Optional[int] = None
    tag_id: Optional[int] = None
    executor: Optional[int] = None
    status: Optional[str] = None


class Color(BaseModel):
    name: str
    value: str


class ColorCreate(Color):
    workspace_id: int


class ColorRead(Color):
    id: int
    workspace_id: int


class ColorUpdate(Color):
    id: int
    name: Optional[str] = None
    value: Optional[str] = None


class Tag(BaseModel):
    name: str


class TagCreate(Tag):
    workspace_id: int


class TagRead(Tag):
    id: int
    workspace_id: int


class TagUpdate(Tag):
    id: int
