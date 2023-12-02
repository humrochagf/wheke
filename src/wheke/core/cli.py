import typer
from rich.console import Console

from wheke.__about__ import __version__

cli = typer.Typer()
console = Console()


@cli.command()
def version() -> None:
    console.print(__version__, highlight=False)
