import os

import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from svcs import Container

from wheke import Pod, Wheke, WhekeSettings, demo_pod, get_settings
from wheke._demo import DEMO_PAGE

from .example_app.settings import AnotherFeatureSettings, CustomFeatureSettings

pytestmark = pytest.mark.anyio


async def test_create_app() -> None:
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
        test: str = "test"

    wheke = Wheke(CustomSettings)
    with TestClient(wheke.create_app()) as app:
        with Container(app.app_state["svcs_registry"]) as container:
            assert get_settings(container, CustomSettings).test == "test"


def test_create_app_with_custom_feature_settings() -> None:
    key = "WHEKE__FEATURES__ANOTHER_FEATURE__TEST_STR"
    os.environ[key] = "expectedvalue"

    wheke = Wheke()
    with TestClient(wheke.create_app()) as app:
        with Container(app.app_state["svcs_registry"]) as container:
            settings = get_settings(container, WhekeSettings)

            custom_feature = settings.get_feature(CustomFeatureSettings)
            assert custom_feature.test_str == "testvalue"

            another_feature = settings.get_feature(AnotherFeatureSettings)
            assert another_feature.test_str == "expectedvalue"
            assert another_feature.test_bool

    os.environ.pop(key, None)


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


def test_state(client: TestClient) -> None:
    response = client.get("/state")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"value": "initialized"}


def test_aping(client: TestClient) -> None:
    response = client.get("/aping")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"value": "apong"}


def test_astate(client: TestClient) -> None:
    response = client.get("/astate")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"value": "initialized"}


def test_custom_settings(client: TestClient) -> None:
    response = client.get("/custom_settings")

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"test_str": "testvalue"}
