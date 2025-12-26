from typing import ClassVar

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from svcs import Container

from ._service import get_service


class FeatureSettings(BaseModel):
    """
    Base model to declare custom feature settings.

    When inheriting from this method make sure to override
    the `__feature_name__` with an unique feature name
    preferentially snake_case lower case (e.g. my_custom_feature).

    The feature name will be used as namespace to the settings values
    defined in the model:

    ```python
    class CustomSettings(FeatureSettings):
        __feature_name__ == "my_feature"
        custom_parameter: str = "test"

    ```

    Can be set like this in the .env file:

    ```.env
    WHEKE_FEATURES='{"my_feature": {"custom_parameter": "custom_value"}}'
    ```
    ```
    """

    __feature_name__: ClassVar[str]
    """
    The namespace of the feature in the app settings.
    """


class WhekeSettings(BaseSettings):
    project_name: str = "Wheke"

    pods: list[str] = Field(default_factory=list)

    features: dict = Field(default_factory=dict)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="wheke_",
        extra="allow",
    )

    def get_feature[T: FeatureSettings](self, cls: type[T]) -> T:
        return cls(**self.features.get(cls.__feature_name__.lower(), {}))


def get_settings[T: WhekeSettings](container: Container, cls: type[T]) -> T:
    return get_service(container, cls)
