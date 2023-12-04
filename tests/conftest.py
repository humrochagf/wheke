import pytest
from fastapi.testclient import TestClient
from typer import Typer

from tests.example_app import wheke


@pytest.fixture
def client() -> TestClient:
    return TestClient(wheke.create_app())


@pytest.fixture
def cli() -> Typer:
    return wheke.create_cli()
