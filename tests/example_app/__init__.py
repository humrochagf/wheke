from pathlib import Path
from typing import Annotated, ClassVar

from fastapi import APIRouter, Depends
from svcs import Container
from svcs.fastapi import DepContainer
from typer import Context, Typer, echo

from wheke import (
    Pod,
    ServiceConfig,
    Wheke,
    WhekeSettings,
    aget_service,
    demo_pod,
    get_container,
    get_service,
    get_settings,
)

STATIC_PATH = Path(__file__).parent / "static"

router = APIRouter()
cli = Typer()


class DBService:
    data: ClassVar[dict] = {
        "ping": "pong",
        "aping": "apong",
    }


def db_service_factory(_: Container) -> DBService:
    return DBService()


class PingService:
    db: DBService

    def __init__(self, db: DBService) -> None:
        self.db = db

    def ping(self) -> str:
        return self.db.data["ping"]


def ping_service_factory(container: Container) -> PingService:
    return PingService(get_service(container, DBService))


def get_ping_service(container: DepContainer) -> PingService:
    return get_service(container, PingService)


PingInjection = Annotated[PingService, Depends(get_ping_service)]


class APingService:
    db: DBService

    def __init__(self, db: DBService) -> None:
        self.db = db

    async def ping(self) -> str:
        return self.db.data["aping"]


async def aping_service_factory(container: Container) -> APingService:
    return APingService(get_service(container, DBService))


async def get_aping_service(container: DepContainer) -> APingService:
    return await aget_service(container, APingService)


APingInjection = Annotated[APingService, Depends(get_aping_service)]


@router.get("/ping")
def ping(service: PingInjection) -> dict:
    return {"value": service.ping()}


@router.get("/aping")
async def aping(service: APingInjection) -> dict:
    return {"value": await service.ping()}


@cli.callback()
def callback() -> None:
    pass


@cli.command()
def ping_cmd(ctx: Context) -> None:
    service = get_service(get_container(ctx), PingService)
    echo(service.ping())


@cli.command()
def service_name_cmd(ctx: Context) -> None:
    settings = get_settings(get_container(ctx), WhekeSettings)
    echo(settings.project_name)


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
