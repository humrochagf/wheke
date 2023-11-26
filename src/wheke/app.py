from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from wheke.auth import router as auth_router
from wheke.auth.repository import AuthRepository, TinyAuthRepository
from wheke.core import settings
from wheke.core.repository import RepositoryRegistry
from wheke.frontend import router as frontend_worker

ROOT_DIR = Path(__file__).parent


def create_app() -> FastAPI:
    app = FastAPI(title=settings.project_name)

    RepositoryRegistry.register(AuthRepository, TinyAuthRepository(settings.auth_db))

    app.mount(
        "/static",
        StaticFiles(directory=ROOT_DIR / "frontend" / "static"),
        name="static",
    )
    app.include_router(auth_router)
    app.include_router(frontend_worker)

    return app


app = create_app()
