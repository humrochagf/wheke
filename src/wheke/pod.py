from pathlib import Path
from typing import Callable

from fastapi import APIRouter
from typer import Typer

from wheke.service import Service

ServiceList = list[tuple[type[Service], Callable]]


class Pod:
    name: str

    router: APIRouter | None

    static_url: str | None
    static_path: Path | None

    services: ServiceList

    cli: Typer | None

    def __init__(
        self,
        name: str,
        *,
        router: APIRouter | None = None,
        static_url: str | None = None,
        static_path: str | Path | None = None,
        services: ServiceList | None = None,
        cli: Typer | None = None,
    ) -> None:
        self.name = name
        self.router = router
        self.static_url = static_url

        if isinstance(static_path, str):
            self.static_path = Path(static_path)
        else:
            self.static_path = static_path

        self.services = services or []
        self.cli = cli
