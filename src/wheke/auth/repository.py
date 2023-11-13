from abc import ABC, abstractmethod

from pydantic_core import to_jsonable_python
from tinydb import TinyDB, where

from wheke.auth.models import UserInDB


class BaseAuthRepository(ABC):
    @abstractmethod
    def get_user(self, username: str) -> UserInDB:
        ...

    @abstractmethod
    def create_user(self, user: UserInDB) -> None:
        ...


class TinyAuthRepository(BaseAuthRepository):
    db: TinyDB

    def __init__(self, connection_string: str) -> None:
        self.db = TinyDB(connection_string, create_dirs=True, encoding="utf-8")

    def get_user(self, username: str) -> UserInDB:
        return UserInDB(**self.db.search(where("username") == username)[0])

    def create_user(self, user: UserInDB) -> None:
        self.db.insert(to_jsonable_python(user))
