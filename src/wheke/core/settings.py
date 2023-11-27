from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "Wheke"

    pods: list[str] = [
        "wheke.auth.auth_pod",
        "wheke.frontend.frontend_pod",
    ]

    # auth
    auth_db: str = "db/auth.json"
    secret_key: SecretStr = SecretStr("change_me")
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_prefix="wheke_", env_file=".env", env_file_encoding="utf-8"
    )


settings = Settings()
