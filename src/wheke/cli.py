from rich.console import Console

from wheke.__about__ import __version__

console = Console()


def version() -> None:
    console.print(__version__, highlight=False)


def empty_callback() -> None:
    pass
