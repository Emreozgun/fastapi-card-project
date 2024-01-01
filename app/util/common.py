from fastapi import Depends, status, Request
from typing import Optional
from jose import jwt, JWTError
from app.backend.config import config
from app.const import (
    AUTH_TOKEN_ALGORITHM, AUTH_URL,
)
from fastapi.security import OAuth2PasswordBearer

from app.exc import raise_with_log
from app.schemas.auth import UserSchema
from app.util.auth import is_expired

oauth2_schema = OAuth2PasswordBearer(tokenUrl=AUTH_URL, auto_error=False)


def get_current_user(
        token: str = Depends(oauth2_schema),
        request: Request = None,
) -> Optional[UserSchema]:
    assert request is not None  # zorunlu kontrol, bu gelmezse 500 error vermeli
    if token is None:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid token")
    try:
        payload = jwt.decode(token, config.token_key, algorithms=[AUTH_TOKEN_ALGORITHM])
        user_uuid: str = payload.get("user")
        expires_at: str = payload.get("expires_at")
        if user_uuid is None:
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
        if is_expired(expires_at):
            raise_with_log(status.HTTP_401_UNAUTHORIZED, "Token expired")

        return UserSchema(user_uuid=user_uuid)
    except JWTError:
        raise_with_log(status.HTTP_401_UNAUTHORIZED, "Invalid credentials")
    raise_with_log(status.HTTP_500_INTERNAL_SERVER_ERROR, "undefined case")
