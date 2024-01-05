from typing import TypeVar

from svcs import Container, Registry

T = TypeVar("T")

_registry = Registry()


def get_service_registry() -> Registry:
    return _registry


def get_service(service_type: type[T]) -> T:
    return Container(_registry).get(service_type)


async def aget_service(service_type: type[T]) -> T:
    return await Container(_registry).aget(service_type)
