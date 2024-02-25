from fastapi import status


class AuthException(Exception):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Unauthorized"
