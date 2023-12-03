import pytest
from fastapi.testclient import TestClient

from wheke.core import Wheke


@pytest.fixture
def client() -> TestClient:
    return TestClient(Wheke().create_app())
