from collections.abc import Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from typer import Typer

from tests.example_app import make_wheke


@pytest.fixture
def client() -> Generator[TestClient, Any, Any]:
    wheke = make_wheke()

    with TestClient(wheke.create_app()) as app:
        yield app


@pytest.fixture
def cli() -> Typer:
    wheke = make_wheke()

    return wheke.create_cli()
