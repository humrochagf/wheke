from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Wheke"

    pods: list[str] = Field(default_factory=list)

    model_config = SettingsConfigDict(
        env_prefix="wheke_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
