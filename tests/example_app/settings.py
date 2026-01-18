from typing import Annotated, ClassVar

from fastapi import Depends
from svcs.fastapi import DepContainer

from wheke import (
    FeatureSettings,
    WhekeSettings,
    get_settings,
)


class CustomSetting(FeatureSettings):
    __feature_name__: ClassVar[str] = "custom_feature"

    test: str = "testvalue"


def _wheke_settings_injection(container: DepContainer) -> WhekeSettings:
    return get_settings(container, WhekeSettings)


WhekeSettingsInjection = Annotated[WhekeSettings, Depends(_wheke_settings_injection)]
