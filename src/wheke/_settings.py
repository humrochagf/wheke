from typing import TypeVar

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from svcs import Registry

from ._service import get_service


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


def get_settings(registry: Registry, cls: type[T]) -> T:
    return get_service(registry, cls)
