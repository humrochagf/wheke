from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from typer import Typer

from tests.example_app import make_wheke


@pytest.fixture
def client() -> Generator[TestClient, Any, Any]:
    wheke = make_wheke()

    yield TestClient(wheke.create_app())

    wheke.close()


@pytest.fixture
def cli() -> Generator[Typer, Any, Any]:
    wheke = make_wheke()

    yield wheke.create_cli()

    wheke.close()
