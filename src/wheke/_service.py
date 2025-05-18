from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

from svcs import Container, Registry

T = TypeVar("T")


@dataclass
class ServiceConfig:
    service_type: type
    service_factory: Callable[[Registry], object]
    health_check: Callable | None = None
    cleanup: Callable | Awaitable | None = None
    as_value: bool = False


def get_service(registry: Registry, service_type: type[T]) -> T:
    return Container(registry).get(service_type)


async def aget_service(registry: Registry, service_type: type[T]) -> T:
    return await Container(registry).aget(service_type)
