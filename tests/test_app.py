from fastapi import FastAPI
from fastapi.testclient import TestClient

from wheke import Wheke
from wheke.demo import DEMO_PAGE, demo_pod


def test_create_app() -> None:
    wheke = Wheke()

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert demo_pod in wheke.pods


def test_demo_pod(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.text == DEMO_PAGE


def test_static(client: TestClient) -> None:
    response = client.get("/static/test.txt")

    assert response.status_code == 200
    assert response.text.strip() == "test"


def test_ping(client: TestClient) -> None:
    response = client.get("/ping")

    assert response.status_code == 200
    assert response.json() == {"value": "pong"}
