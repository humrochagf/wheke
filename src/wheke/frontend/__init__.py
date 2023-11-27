from pathlib import Path

from wheke.core.pod import Pod
from wheke.frontend.routes import router

frontend_pod = Pod(
    "frontend",
    Path(__file__).parent,
    router=router,
    static_url="/static",
    static_folder="static",
)
