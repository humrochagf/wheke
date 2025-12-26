from collections.abc import Awaitable, Callable
from dataclasses import dataclass

from svcs import Container


@dataclass
class ServiceConfig:
    service_type: type
    service_factory: Callable[[Container], object]
    health_check: Callable | None = None
    cleanup: Callable | Awaitable | None = None
    as_value: bool = False


def get_service[T](container: Container, service_type: type[T]) -> T:
    return container.get(service_type)


async def aget_service[T](container: Container, service_type: type[T]) -> T:
    return await container.aget(service_type)
