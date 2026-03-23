from typing import Annotated, ClassVar

from fastapi import Depends
from svcs.fastapi import DepContainer

from wheke import (
    FeatureSettings,
    WhekeSettings,
    get_settings,
)


class CustomFeatureSettings(FeatureSettings):
    __feature_name__: ClassVar[str] = "custom_feature"

    test_str: str = "testvalue"


class AnotherFeatureSettings(FeatureSettings):
    __feature_name__: ClassVar[str] = "another_feature"

    test_str: str = "anothervalue"

    test_bool: bool = True


def _wheke_settings_injection(container: DepContainer) -> WhekeSettings:
    return get_settings(container, WhekeSettings)


WhekeSettingsInjection = Annotated[WhekeSettings, Depends(_wheke_settings_injection)]
