from fastapi import FastAPI, status
from fastapi.testclient import TestClient

from wheke import Pod, Wheke, WhekeSettings, demo_pod, get_settings
from wheke._demo import DEMO_PAGE


def test_create_app() -> None:
    wheke = Wheke()

    app = wheke.create_app()

    assert type(app) is FastAPI


def test_create_app_with_demo_pod_in_settings() -> None:
    settings = WhekeSettings()
    settings.pods = ["wheke.demo_pod"]

    wheke = Wheke(settings)

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert demo_pod in wheke.pods


def test_create_app_with_empty_pod() -> None:
    empty_pod = Pod("empty")
    wheke = Wheke()
    wheke.add_pod(empty_pod)

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert wheke.pods == [empty_pod]


def test_create_app_with_custom_settings_class() -> None:
    class CustomSettings(WhekeSettings):
        test_setting: str = "test"

    wheke = Wheke(CustomSettings)

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert get_settings(CustomSettings).test_setting == "test"


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
