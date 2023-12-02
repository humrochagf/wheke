from abc import ABC
from typing import Callable

from wheke.core.exceptions import ServiceTypeNotRegistered


class Service(ABC):
    pass


class ServiceRegistry:
    _registry: dict[type[Service], Callable[[], Service]] = {}

    @classmethod
    def register(
        cls,
        service_type: type[Service],
        service_factory: Callable[[], Service],
    ) -> None:
        cls._registry[service_type] = service_factory

    @classmethod
    def get(cls, service_type: type[Service]) -> Service:
        service_factory = cls._registry.get(service_type)

        if not service_factory:
            raise ServiceTypeNotRegistered

        return service_factory()
