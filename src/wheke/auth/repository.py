from abc import abstractmethod
from functools import partial
from typing import Callable, cast

from aiotinydb.database import AIOTinyDB
from pydantic_core import to_jsonable_python
from tinydb import where

from wheke.auth.models import UserInDB
from wheke.core.repository import Repository, RepositoryRegistry
from wheke.core.settings import settings


class AuthRepository(Repository):
    @abstractmethod
    async def get_user(self, username: str) -> UserInDB:
        ...

    @abstractmethod
    async def create_user(self, user: UserInDB) -> None:
        ...


class TinyAuthRepository(AuthRepository):
    db_factory: Callable[[], AIOTinyDB]

    def __init__(self, connection_string: str) -> None:
        self.db_factory = partial(
            AIOTinyDB, connection_string, create_dirs=True, encoding="utf-8"
        )

    async def get_user(self, username: str) -> UserInDB:
        async with self.db_factory() as db:
            return UserInDB(**db.search(where("username") == username)[0])

    async def create_user(self, user: UserInDB) -> None:
        async with self.db_factory() as db:
            db.insert(to_jsonable_python(user))


def make_repository() -> AuthRepository:
    return TinyAuthRepository(settings.auth_db)


def get_repository() -> AuthRepository:
    return cast(AuthRepository, RepositoryRegistry.get(AuthRepository))
