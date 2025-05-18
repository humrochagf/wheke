from typer import Typer
from typer.testing import CliRunner

from wheke import Wheke
from wheke.__about__ import __version__
from wheke.__main__ import cli as main_cli

runner = CliRunner()


def test_create_cli() -> None:
    wheke = Wheke()
    app = wheke.create_cli()

    assert type(app) is Typer


def test_version() -> None:
    result = runner.invoke(main_cli, "version")

    assert result.exit_code == 0
    assert result.stdout.strip() == __version__


def test_ping_cmd(cli: Typer) -> None:
    result = runner.invoke(cli, ["test", "ping-cmd"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "pong"


def test_service_name_cmd(cli: Typer) -> None:
    result = runner.invoke(cli, ["test", "service-name-cmd"])

    assert result.exit_code == 0
    assert result.stdout.strip() == "Wheke"
