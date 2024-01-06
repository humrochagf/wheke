from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from wheke import Wheke
from wheke.demo import DEMO_PAGE, demo_pod
from wheke.pod import Pod
from wheke.settings import settings


def test_create_app() -> None:
    wheke = Wheke()

    app = wheke.create_app()

    assert type(app) is FastAPI


def test_create_app_with_demo_pod_in_settings() -> None:
    before_pods = settings.pods.copy()
    settings.pods = ["wheke.demo.demo_pod"]

    wheke = Wheke()

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert demo_pod in wheke.pods

    settings.pods = before_pods


def test_create_app_with_empty_pod() -> None:
    empty_pod = Pod("empty")
    wheke = Wheke()
    wheke.add_pod(empty_pod)

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert wheke.pods == [empty_pod]


def test_demo_pod(client: TestClient) -> None:
    response = client.get("/")

    assert response.status_code == status.HTTP_200_OK
    assert response.text == DEMO_PAGE


def test_static(client: TestClient) -> None:
    response = client.get("/static/test.txt")

    assert response.status_code == status.HTTP_200_OK
    assert response.text.strip() == "test"


def test_ping(client: TestClient) -> None:
    response = client.get("/ping")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"value": "pong"}


def test_aping(client: TestClient) -> None:
    response = client.get("/aping")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"value": "pong"}
