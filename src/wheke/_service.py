from collections.abc import Callable
from dataclasses import dataclass

from svcs import Container


@dataclass
class ServiceConfig:
    service_type: type
    service_factory: Callable[[Container], object]
    health_check: Callable | None = None

    is_singleton: bool = False
    singleton_cleanup_method: str = ""

    def get_cleanup_method(self, service: object) -> Callable | None:
        if self.singleton_cleanup_method and hasattr(
            service, self.singleton_cleanup_method
        ):
            return getattr(service, self.singleton_cleanup_method)

        return None


def get_service[T](container: Container, service_type: type[T]) -> T:
    return container.get(service_type)


async def aget_service[T](container: Container, service_type: type[T]) -> T:
    return await container.aget(service_type)
