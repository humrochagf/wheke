from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import TypeVar

from svcs import Container
from typer import Context

from wheke._constants import KEY_REGISTRY

T = TypeVar("T")


@dataclass
class ServiceConfig:
    service_type: type
    service_factory: Callable[[Container], object]
    health_check: Callable | None = None
    cleanup: Callable | Awaitable | None = None
    as_value: bool = False


def get_service(container: Container, service_type: type[T]) -> T:
    return container.get(service_type)


async def aget_service(container: Container, service_type: type[T]) -> T:
    return await container.aget(service_type)


def get_service_from_context(ctx: Context, service_type: type[T]) -> T:
    registry = ctx.obj[KEY_REGISTRY]

    with Container(registry) as container:
        return container.get(service_type)
