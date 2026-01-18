from fastapi import APIRouter

from .services import APingInjection, PingInjection
from .settings import CustomSetting, WhekeSettingsInjection

router = APIRouter()


@router.get("/ping")
def ping(service: PingInjection) -> dict:
    return {"value": service.ping()}


@router.get("/state")
def state(service: PingInjection) -> dict:
    return {"value": service.get_state()}


@router.get("/aping")
async def aping(service: APingInjection) -> dict:
    return {"value": await service.ping()}


@router.get("/astate")
async def astate(service: APingInjection) -> dict:
    return {"value": await service.get_state()}


@router.get("/custom_settings")
async def custom_settings(settings: WhekeSettingsInjection) -> dict:
    return settings.get_feature(CustomSetting).model_dump()
