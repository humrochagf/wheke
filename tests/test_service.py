import pytest

from wheke.exceptions import ServiceTypeNotRegisteredError
from wheke.service import Service, ServiceRegistry


def test_service_not_registered() -> None:
    class NotRegistered(Service):
        pass

    with pytest.raises(ServiceTypeNotRegisteredError):
        ServiceRegistry.get(NotRegistered)
