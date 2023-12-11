from pathlib import Path
from typing import Annotated, cast

from fastapi import APIRouter, Depends
from typer import Typer, echo

from wheke import Pod, Service, ServiceRegistry, Wheke

STATIC_PATH = Path(__file__).parent / "static"

router = APIRouter()
cli = Typer()


class TestService(Service):
    def ping(self) -> str:
        return "pong"


def test_service_factory() -> TestService:
    return TestService()


def get_test_service() -> TestService:
    return cast(TestService, ServiceRegistry.get(TestService))


@router.get("/ping")
def ping(service: Annotated[TestService, Depends(get_test_service)]) -> dict:
    return {"value": service.ping()}


@cli.callback()
def callback() -> None:
    pass


@cli.command()
def hello() -> None:
    echo("world")


test_pod = Pod(
    "test",
    router=router,
    static_url="/static",
    static_path=str(STATIC_PATH),
    services=[(TestService, test_service_factory)],
    cli=cli,
)

wheke = Wheke()
wheke.add_pod(test_pod)
