from collections.abc import Callable
from pathlib import Path

from fastapi import APIRouter
from typer import Typer

ServiceList = list[tuple[type, Callable]]


class Pod:
    """
    A Pod is the base unity that controls a funcionality.
    """

    name: str
    "The name of the Pod."

    router: APIRouter | None
    """
    The router from `fastapi.APIRouter` that contains
    all the routes for the Pod.
    """

    static_url: str | None
    "The url prefix for the Pod static files."

    static_path: Path | None
    "The path to the Pod static files."

    services: ServiceList
    """
    The list of services provided by the Pod.

    It consists of a tuple of the service class
    and the service factory callable.
    """

    cli: Typer | None
    "The Typer cli of the Pod"

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
