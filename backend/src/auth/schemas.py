import datetime
from typing import Union, Optional, List

from pydantic import BaseModel, EmailStr

from src.auth.models import UserRole
from src.workspace.models import Workspace


class UserBase(BaseModel):
    username: str
    telegram_name: str
    email: EmailStr
    role: UserRole

    class ConfigDict:
        from_attributes = True


class UserCreate(UserBase):
    password: str

    class ConfigDict:
        from_attributes = True


class UserRead(UserBase):
    id: int
    registered_at: datetime.datetime
    is_active: bool
    workspaces: Optional[List] = None

    class ConfigDict:
        from_attributes = True


class UserUpdate(BaseModel):
    username: Optional[str] = None
    telegram_name: Optional[str] = None
    role: Optional[UserRole] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    workspaces: Optional[List] = []

    class ConfigDict:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str


class UserUpdateWorkspace(BaseModel):
    id: int
    workspaces: Union[List, int]
