from rich.console import Console
from svcs import Container
from typer import Context

from wheke._constants import KEY_CONTAINER

from .__about__ import __version__

console = Console()


def version() -> None:
    console.print(__version__, highlight=False)


def get_container(ctx: Context) -> Container:
    return ctx.obj[KEY_CONTAINER]
