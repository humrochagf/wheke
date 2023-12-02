from pathlib import Path
from typing import Callable

from fastapi import APIRouter
from typer import Typer

from wheke.core.repository import Repository

RepositoriesList = list[tuple[type[Repository], Callable]]


class Pod:
    name: str
    root_path: Path

    router: APIRouter | None

    static_url: str | None
    static_folder: str | None

    repositories: RepositoriesList

    cli: Typer | None

    def __init__(
        self,
        name: str,
        root_path: Path,
        *,
        router: APIRouter | None = None,
        static_url: str | None = None,
        static_folder: str | None = None,
        repositories: RepositoriesList | None = None,
        cli: Typer | None = None,
    ) -> None:
        self.name = name
        self.root_path = root_path
        self.router = router
        self.static_url = static_url
        self.static_folder = static_folder
        self.repositories = repositories or []
        self.cli = cli
