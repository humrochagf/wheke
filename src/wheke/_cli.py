from rich.console import Console

from .__about__ import __version__

console = Console()


def version() -> None:
    console.print(__version__, highlight=False)


def empty_callback() -> None:
    pass
