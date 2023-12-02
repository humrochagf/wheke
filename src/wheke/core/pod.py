from pathlib import Path
from typing import Callable

from fastapi import APIRouter
from typer import Typer

from wheke.core.service import Service

ServiceList = list[tuple[type[Service], Callable]]


class Pod:
    name: str
    root_path: Path

    router: APIRouter | None

    static_url: str | None
    static_folder: str | None

    services: ServiceList

    cli: Typer | None

    def __init__(
        self,
        name: str,
        root_path: Path,
        *,
        router: APIRouter | None = None,
        static_url: str | None = None,
        static_folder: str | None = None,
        services: ServiceList | None = None,
        cli: Typer | None = None,
    ) -> None:
        self.name = name
        self.root_path = root_path
        self.router = router
        self.static_url = static_url
        self.static_folder = static_folder
        self.services = services or []
        self.cli = cli
