from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from wheke.auth.exceptions import AuthException
from wheke.auth.models import Token, TokenData, User, UserInDB
from wheke.auth.repository import TinyAuthRepository
from wheke.core import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

repository = TinyAuthRepository(settings.auth_db)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str) -> UserInDB | None:
    user = repository.get_user(username)

    if user and verify_password(password, user.hashed_password):
        return user

    return None


def create_access_token(data: dict) -> Token:
    to_encode = data.copy()
    expiration = datetime.now(tz=timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    to_encode.update({"exp": expiration})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key.get_secret_value(), algorithm=ALGORITHM
    )

    return Token(access_token=encoded_jwt, token_type="bearer")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    try:
        payload = jwt.decode(
            token, settings.secret_key.get_secret_value(), algorithms=[ALGORITHM]
        )
        username: str | None = payload.get("sub")

        if username is None:
            raise AuthException

        token_data = TokenData(username=username)
    except JWTError as ex:
        raise AuthException from ex

    user = repository.get_user(token_data.username)

    if user is None:
        raise AuthException

    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user
