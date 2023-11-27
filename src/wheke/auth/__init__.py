from pathlib import Path

from wheke.auth.repository import AuthRepository, make_repository
from wheke.auth.routes import router
from wheke.core.pod import Pod

auth_pod = Pod(
    "auth",
    Path(__file__).parent,
    router=router,
    repositories=[(AuthRepository, make_repository)],
)
