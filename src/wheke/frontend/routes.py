from pathlib import Path

from fastapi import APIRouter, Request, Response
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

ROOT_DIR = Path(__file__).parent.resolve()

router = APIRouter()
templates = Jinja2Templates(directory=ROOT_DIR / "templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index(request: Request) -> Response:
    return templates.TemplateResponse("index.html", {"request": request})
