from abc import ABC
from typing import Callable

from wheke.core.exceptions import RepositoryNotSetException


class Repository(ABC):
    pass


class RepositoryRegistry:
    _registry: dict[type[Repository], Callable[[], Repository]] = {}

    @classmethod
    def register(
        cls,
        repository_type: type[Repository],
        repository_factory: Callable[[], Repository],
    ) -> None:
        cls._registry[repository_type] = repository_factory

    @classmethod
    def get(cls, repository_type: type[Repository]) -> Repository:
        repository = cls._registry.get(repository_type)

        if not repository:
            raise RepositoryNotSetException

        return repository()
