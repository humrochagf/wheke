from typing import Annotated, ClassVar

from fastapi import Depends
from svcs import Container
from svcs.fastapi import DepContainer

from wheke import (
    aget_service,
    get_service,
)


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
