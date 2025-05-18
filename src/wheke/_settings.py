from typing import TypeVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from svcs import Container
from typer import Context

from ._service import get_service, get_service_from_context


class WhekeSettings(BaseSettings):
    project_name: str = "Wheke"

    pods: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="wheke_",
        extra="allow",
    )


T = TypeVar("T", bound=WhekeSettings)


def get_settings(container: Container, cls: type[T]) -> T:
    return get_service(container, cls)


def get_settings_from_context(ctx: Context, cls: type[T]) -> T:
    return get_service_from_context(ctx, cls)
