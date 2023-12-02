import asyncio

import typer
from rich.console import Console
from rich.prompt import Prompt

from wheke.auth.models import User
from wheke.auth.repository import get_repository
from wheke.auth.security import create_user

cli = typer.Typer()
console = Console()


@cli.command()
def createuser() -> None:
    """
    Create a User and store it in the service db.
    """
    full_name = Prompt.ask("Enter the full name for the user")
    username = Prompt.ask("Enter the username for the user")

    if asyncio.run(get_repository().get_user(username)):
        console.print(f"The username [red]{username}[/] already exists")

        raise typer.Abort()

    email = Prompt.ask("Enter the email for the user")

    user = User(
        username=username,
        full_name=full_name,
        email=email,
    )

    password = Prompt.ask("Enter a password for the user", password=True)

    asyncio.run(create_user(user, password))

    console.print(f"The user [green]{username}[/] got created!")
