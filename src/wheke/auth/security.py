from typing import Annotated, cast

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from wheke.auth.exceptions import AuthException
from wheke.auth.models import User, UserInDB
from wheke.auth.service import AuthService, get_auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserInDB:
    token_data = service.decode_access_token_data(token)
    user = await service.get_user(token_data.username)

    if user is None:
        raise AuthException

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
