from fastapi import APIRouter, Response
from fastapi.responses import HTMLResponse

from wheke.pod import Pod

DEMO_PAGE = """
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    .m-0{margin:0;}
    .h-100vh{height:100vh;}
    .max-w-100vw{max-width:100vw;}
    .flex{display:flex;}
    .flex-col{flex-direction:column;}
    .justify-between{justify-content:space-between;}
    .p-3{padding:0.75rem;}
    .text-center{text-align:center;}
    .text-6xl{font-size:3.75rem;line-height:1;}
    .font-black{font-weight:900;}
    .font-sans{font-family: Arial, sans-serif;}
  </style>
</head>
<body class="text-center flex flex-col justify-between h-100vh m-0">
  <div>
    <h1 class="font-sans font-black text-6xl">Wheke</h1>
    <img class="max-w-100vw" src="" alt="Wheke"></a>
    <br>
    <em>A cute framework for small self-hosted apps</em>
  </div>
  <div class="p-3">
    <small>Made with ❤️ by
    <a href="https://humberto.io">Humberto Rocha</a></small>
    <br>
    <small>Illustrated with ❤️ by
    <a href="https://bissgigi.art">Giovanna Bissacot</a></small>
  </div>
</body>
</html>
"""

router = APIRouter()


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def index() -> Response:
    return HTMLResponse(DEMO_PAGE)


demo_pod = Pod("demo", router=router)
