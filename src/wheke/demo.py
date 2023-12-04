from pathlib import Path

from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse

from wheke.pod import Pod

STATIC_PATH = Path(__file__).resolve().parent / "static"

DEMO_PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      text-align: center;
      height: 100vh;
      margin: 0;
    }
    h1 {
      font-family: Arial, sans-serif;
      font-weight: 900;
      font-size: 3.75rem;
      line-height: 1;
    }
    main {
      padding: 0 1rem 5rem 1rem;
    }
    img {
        max-width: 100%;
    }
    footer {
      padding: 1rem;
    }
  </style>
</head>
<body>
  <header>
    <h1>Wheke</h1>
  </header>
  <main>
    <img src="/static/demo/wheke.png" alt="Wheke"></a>
    <br>
    <em>A cute framework for small self-hosted apps</em>
  </main>
  <footer>
    <small>Made with ❤️ by
    <a href="https://humberto.io">Humberto Rocha</a></small>
    <br>
    <small>Illustrated with ❤️ by
    <a href="https://bissgigi.art">Giovanna Bissacot</a></small>
  </footer>
</body>
</html>
"""

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index() -> Response:
    return HTMLResponse(DEMO_PAGE)


demo_pod = Pod(
    "demo",
    router=router,
    static_url="/static/demo",
    static_path=STATIC_PATH,
)
