from datetime import datetime, timedelta, timezone
from typing import cast

from jose import JWTError, jwt
from passlib.context import CryptContext

from wheke.auth.exceptions import AuthException
from wheke.auth.models import Token, TokenData, User, UserInDB
from wheke.auth.repository import AuthRepository, TinyAuthRepository
from wheke.core.service import Service, ServiceRegistry
from wheke.core.settings import settings

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService(Service):
    repository: AuthRepository

    def __init__(self, repository: AuthRepository) -> None:
        self.repository = repository

    def decode_access_token_data(self, token: str) -> TokenData:
        try:
            payload = jwt.decode(
                token, settings.secret_key.get_secret_value(), algorithms=[ALGORITHM]
            )
            username: str | None = payload.get("sub")

            if username is None:
                raise AuthException

            return TokenData(username=username)
        except JWTError as ex:
            raise AuthException from ex

    def create_access_token(self, data: dict) -> Token:
        to_encode = data.copy()
        expiration = datetime.now(tz=timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
        to_encode.update({"exp": expiration})
        encoded_jwt = jwt.encode(
            to_encode, settings.secret_key.get_secret_value(), algorithm=ALGORITHM
        )

        return Token(access_token=encoded_jwt, token_type="bearer")

    async def authenticate_user(self, username: str, password: str) -> UserInDB | None:
        user = await self.get_user(username)

        if user and pwd_context.verify(password, user.hashed_password):
            return user

        return None

    async def get_user(self, username: str) -> UserInDB | None:
        return await self.repository.get_user(username)

    async def create_user(self, user: User, password: str) -> None:
        user = UserInDB(
            hashed_password=pwd_context.hash(password), **(user.model_dump())
        )
        await self.repository.create_user(user)


def auth_service_factory() -> AuthService:
    return AuthService(TinyAuthRepository(settings.auth_db))


def get_auth_service() -> AuthService:
    return cast(AuthService, ServiceRegistry.get(AuthService))
