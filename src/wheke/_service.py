from collections.abc import Callable
from dataclasses import dataclass
from typing import TypeVar

from svcs import Container, Registry

T = TypeVar("T")

_registry: Registry = Registry()


@dataclass
class ServiceConfig:
    service_type: type
    service_factory: Callable
    as_value: bool = False


def close_service_registry() -> None:
    _registry.close()


async def aclose_service_registry() -> None:
    await _registry.aclose()


def register_service(config: ServiceConfig) -> bool:
    if config.as_value:
        _registry.register_value(config.service_type, config.service_factory())
    else:
        _registry.register_factory(config.service_type, config.service_factory)

    return True


def get_service(service_type: type[T]) -> T:
    return Container(_registry).get(service_type)


async def aget_service(service_type: type[T]) -> T:
    return await Container(_registry).aget(service_type)
