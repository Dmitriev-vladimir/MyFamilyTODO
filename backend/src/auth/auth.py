import functools
from datetime import timedelta, datetime
from typing import Optional, Type

from fastapi import HTTPException, status, Depends
from fastapi.security import APIKeyHeader
# from passlib.context import CryptContext
from passlib.hash import pbkdf2_sha256
from jose import jwt, JWTError
from fastapi.responses import Response
from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# from src.settings import settings
from settings import config as settings
from src.auth.models import User
from src.db.database import get_async_session
from src.exceptions import AuthException

# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

apikey_scheme = APIKeyHeader(name="Authorization")


class Hasher:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pbkdf2_sha256.verify(plain_password, hashed_password)
        # return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pbkdf2_sha256.hash(password)
        # return pwd_context.hash(password)


def get_token(data: dict, expires_delta: timedelta = timedelta(days=3)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_payload_from_token(token: str):
    try:
        return jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        raise AuthException


def authenticate_user(user: User, password: str) -> Optional[dict]:
    if isinstance(user.id, int):
        if Hasher.verify_password(password, user.hashed_password):
            res = {
                'access_token': get_token({
                    'id': user.id,
                    'role': str(user.role.value),
                }, expires_delta=timedelta(minutes=30)),
                'refresh_token': get_token({
                    'id': user.id,
                    # 'control_string'
                })
            }
            return res
    return None


async def refresh_token(token: str, session: AsyncSession) -> Optional[dict]:
    token_data = get_payload_from_token(token)
    if token_data.get('id'):
        # user = await get_user_by_id(token_data.get('id'), session)
        user = await session.get(User, token_data.get('id'))
        if user is None:
            return
        return {
            'access_token': get_token({
                'id': user.id,
                'role': str(user.role.value),
            }, expires_delta=timedelta(minutes=30)),
            'refresh_token': get_token({
                'id': user.id,
            })
        }
    return


def authentication(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        request_token = kwargs.get('Authorization')
        if request_token is None or not request_token.startswith('JWT '):
            return Response(status_code=AuthException.status_code, content=AuthException.detail)
        payload = get_payload_from_token(request_token.replace('JWT ', ''))
        session = kwargs['session']
        # user = await get_user_by_id(payload.get('id'), session)
        # kwargs['current_user'] = user
        return await func(*args, **kwargs)

    return wrapper
