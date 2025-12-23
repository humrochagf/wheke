from importlib import metadata

from rich.console import Console
from svcs import Container
from typer import Context

from wheke._constants import KEY_CONTAINER

console = Console()


def version() -> None:
    console.print(metadata.version("wheke"), highlight=False)


def get_container(ctx: Context) -> Container:
    return ctx.obj[KEY_CONTAINER]
