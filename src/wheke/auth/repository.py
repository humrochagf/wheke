from abc import abstractmethod
from functools import partial
from typing import Callable

from aiotinydb.database import AIOTinyDB
from pydantic_core import to_jsonable_python
from tinydb import where

from wheke.auth.models import UserInDB


class AuthRepository:
    @abstractmethod
    async def get_user(self, username: str) -> UserInDB | None:
        ...

    @abstractmethod
    async def create_user(self, user: UserInDB) -> None:
        ...


class TinyAuthRepository(AuthRepository):
    db_factory: Callable[[], AIOTinyDB]

    def __init__(self, connection_string: str) -> None:
        self.db_factory = partial(AIOTinyDB, connection_string)

    async def get_user(self, username: str) -> UserInDB | None:
        async with self.db_factory() as db:
            if result := db.search(where("username") == username):
                return UserInDB(**result[0])
        return None

    async def create_user(self, user: UserInDB) -> None:
        async with self.db_factory() as db:
            db.insert(to_jsonable_python(user))
