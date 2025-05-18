from pathlib import Path
from typing import ClassVar

from fastapi import APIRouter
from svcs import Registry
from svcs.fastapi import DepContainer
from typer import Typer, echo

from wheke import Pod, ServiceConfig, Wheke, demo_pod
from wheke._service import get_service

STATIC_PATH = Path(__file__).parent / "static"

router = APIRouter()
cli = Typer()


class DBService:
    data: ClassVar[dict] = {
        "ping": "pong",
        "aping": "apong",
    }


def db_service_factory(_: Registry) -> DBService:
    return DBService()


class PingService:
    db: DBService

    def __init__(self, db: DBService) -> None:
        self.db = db

    def ping(self) -> str:
        return self.db.data["ping"]


def ping_service_factory(registry: Registry) -> PingService:
    return PingService(get_service(registry, DBService))


class APingService:
    db: DBService

    def __init__(self, db: DBService) -> None:
        self.db = db

    async def ping(self) -> str:
        return self.db.data["aping"]


async def aping_service_factory(registry: Registry) -> APingService:
    return APingService(get_service(registry, DBService))


@router.get("/ping")
def ping(services: DepContainer) -> dict:
    service = services.get(PingService)
    return {"value": service.ping()}


@router.get("/aping")
async def aping(services: DepContainer) -> dict:
    service = await services.aget(APingService)
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
        ServiceConfig(DBService, db_service_factory, as_value=True),
        ServiceConfig(PingService, ping_service_factory),
        ServiceConfig(APingService, aping_service_factory),
    ],
    cli=cli,
)


def make_wheke() -> Wheke:
    wheke = Wheke()
    wheke.add_pod(demo_pod)
    wheke.add_pod(test_pod)

    return wheke
