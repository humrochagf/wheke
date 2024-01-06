from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends
from typer import Typer, echo

from wheke import Pod, Wheke, get_service
from wheke.demo import demo_pod
from wheke.service import aget_service

STATIC_PATH = Path(__file__).parent / "static"

router = APIRouter()
cli = Typer()


class PingService:
    def ping(self) -> str:
        return "pong"


def ping_service_factory() -> PingService:
    return PingService()


def get_ping_service() -> PingService:
    return get_service(PingService)


class APingService:
    async def ping(self) -> str:
        return "pong"


async def aping_service_factory() -> APingService:
    return APingService()


async def get_aping_service() -> APingService:
    return await aget_service(APingService)


@router.get("/ping")
def ping(service: Annotated[PingService, Depends(get_ping_service)]) -> dict:
    return {"value": service.ping()}


@router.get("/aping")
async def aping(service: Annotated[APingService, Depends(get_aping_service)]) -> dict:
    return {"value": await service.ping()}


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
    services=[
        (PingService, ping_service_factory),
        (APingService, aping_service_factory),
    ],
    cli=cli,
)

wheke = Wheke()
wheke.add_pod(demo_pod)
wheke.add_pod(test_pod)
