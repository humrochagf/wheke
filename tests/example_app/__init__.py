from pathlib import Path
from typing import Annotated, ClassVar

from fastapi import APIRouter, Depends
from svcs import Container
from svcs.fastapi import DepContainer
from typer import Context, Typer, echo

from wheke import (
    FeatureSettings,
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


class StateService:
    state: str

    def __init__(self) -> None:
        self.state = "initialized"

    def dispose(self) -> None:
        self.state = "disposed"


def state_service_factory(_: Container) -> StateService:
    return StateService()


class AStateService:
    state: str

    def __init__(self) -> None:
        self.state = "initialized"

    async def dispose(self) -> None:
        self.state = "disposed"


def astate_service_factory(_: Container) -> AStateService:
    return AStateService()


class PingService:
    db: DBService
    state: StateService

    def __init__(self, db: DBService, state: StateService) -> None:
        self.db = db
        self.state = state

    def ping(self) -> str:
        return self.db.data["ping"]

    def get_state(self) -> str:
        return self.state.state


def ping_service_factory(container: Container) -> PingService:
    return PingService(
        get_service(container, DBService),
        get_service(container, StateService),
    )


def get_ping_service(container: DepContainer) -> PingService:
    return get_service(container, PingService)


PingInjection = Annotated[PingService, Depends(get_ping_service)]


class APingService:
    db: DBService
    state: AStateService

    def __init__(self, db: DBService, state: AStateService) -> None:
        self.db = db
        self.state = state

    async def ping(self) -> str:
        return self.db.data["aping"]

    async def get_state(self) -> str:
        return self.state.state


async def aping_service_factory(container: Container) -> APingService:
    return APingService(
        get_service(container, DBService),
        get_service(container, AStateService),
    )


async def get_aping_service(container: DepContainer) -> APingService:
    return await aget_service(container, APingService)


APingInjection = Annotated[APingService, Depends(get_aping_service)]


class CustomSetting(FeatureSettings):
    __feature_name__: ClassVar[str] = "custom_feature"

    test: str = "testvalue"


def _wheke_settings_injection(container: DepContainer) -> WhekeSettings:
    return get_settings(container, WhekeSettings)


WhekeSettingsInjection = Annotated[WhekeSettings, Depends(_wheke_settings_injection)]


@router.get("/ping")
def ping(service: PingInjection) -> dict:
    return {"value": service.ping()}


@router.get("/state")
def state(service: PingInjection) -> dict:
    return {"value": service.get_state()}


@router.get("/aping")
async def aping(service: APingInjection) -> dict:
    return {"value": await service.ping()}


@router.get("/astate")
async def astate(service: APingInjection) -> dict:
    return {"value": await service.get_state()}


@router.get("/custom_settings")
async def custom_settings(settings: WhekeSettingsInjection) -> dict:
    return settings.get_feature(CustomSetting).model_dump()


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
        ServiceConfig(DBService, db_service_factory, is_singleton=True),
        ServiceConfig(
            StateService,
            state_service_factory,
            is_singleton=True,
            singleton_cleanup_method="dispose",
        ),
        ServiceConfig(
            AStateService,
            astate_service_factory,
            is_singleton=True,
            singleton_cleanup_method="dispose",
        ),
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
