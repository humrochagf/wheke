from typer import Context, Typer, echo

from wheke import (
    WhekeSettings,
    get_container,
    get_service,
    get_settings,
)

from .services import PingService

cli = Typer()


@cli.callback()
def callback() -> None:
    pass


@cli.command()
def ping_cmd(ctx: Context) -> None:
    service = get_service(get_container(ctx), PingService)
    echo(service.ping())


@cli.command()
def service_name_cmd(ctx: Context) -> None:
    settings = get_settings(get_container(ctx), WhekeSettings)
    echo(settings.project_name)
