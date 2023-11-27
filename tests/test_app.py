from fastapi import FastAPI

from wheke import Wheke
from wheke.auth import auth_pod
from wheke.frontend import frontend_pod


def test_create_app() -> None:
    wheke = Wheke()

    app = wheke.create_app()

    assert type(app) is FastAPI
    assert auth_pod in wheke.pods
    assert frontend_pod in wheke.pods
