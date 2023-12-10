from abc import ABC
from collections.abc import Callable
from typing import ClassVar

from wheke.exceptions import ServiceTypeNotRegisteredError


class Service(ABC):
    """
    The Service base class that all Wheke
    services must implement.
    """

    pass


class ServiceRegistry:
    """
    ServiceRegistry used to register and get services.
    """

    _registry: ClassVar[dict[type[Service], Callable[[], Service]]] = {}

    @classmethod
    def register(
        cls,
        service_type: type[Service],
        service_factory: Callable[[], Service],
    ) -> None:
        """
        Register a service by providing its class
        and the service factory callable.
        """
        cls._registry[service_type] = service_factory

    @classmethod
    def get(cls, service_type: type[Service]) -> Service:
        """
        Get a service by its class.
        """
        service_factory = cls._registry.get(service_type)

        if not service_factory:
            raise ServiceTypeNotRegisteredError

        return service_factory()
