from pathlib import Path

from wheke import (
    Pod,
    ServiceConfig,
)

from .cli import cli
from .routes import router
from .services import (
    APingService,
    AStateService,
    DBService,
    PingService,
    StateService,
    aping_service_factory,
    astate_service_factory,
    db_service_factory,
    ping_service_factory,
    state_service_factory,
)

STATIC_PATH = Path(__file__).parent / "static"

test_pod = Pod(
    "test",
    router=router,
    static_url="/static",
    static_path=str(STATIC_PATH),
    services=[
        ServiceConfig(DBService, db_service_factory, is_singleton=True),
        ServiceConfig(
            StateService,
            state_service_factory,
            is_singleton=True,
            singleton_cleanup_method="dispose",
        ),
        ServiceConfig(
            AStateService,
            astate_service_factory,
            is_singleton=True,
            singleton_cleanup_method="dispose",
        ),
        ServiceConfig(PingService, ping_service_factory),
        ServiceConfig(APingService, aping_service_factory),
    ],
    cli=cli,
)
