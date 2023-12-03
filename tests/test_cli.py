from typer import Typer
from typer.testing import CliRunner

from wheke import Wheke
from wheke.__about__ import __version__
from wheke.demo import demo_pod

runner = CliRunner()


def test_create_cli() -> None:
    wheke = Wheke()

    app = wheke.create_cli()

    assert type(app) is Typer
    assert demo_pod in wheke.pods


def test_version() -> None:
    app = Wheke().create_cli()

    result = runner.invoke(app, "version")

    assert result.exit_code == 0
    assert result.stdout.strip() == __version__
