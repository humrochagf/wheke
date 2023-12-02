from pathlib import Path

from wheke.auth.cli import cli
from wheke.auth.routes import router
from wheke.auth.service import AuthService, auth_service_factory
from wheke.core.pod import Pod

auth_pod = Pod(
    "auth",
    Path(__file__).parent,
    router=router,
    services=[(AuthService, auth_service_factory)],
    cli=cli,
)
