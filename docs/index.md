<p align="center">
  <img src="wheke.png" alt="Wheke"></a>
</p>

<p align="center">
  <em>A cute framework for small self-hosted apps</em>
  <br/>
  <em><sup><sub>artwork by <a href="https://bissgigi.art/">@bissgigi</a></sub></sup></em>
</p>

<p align="center">
  <a href="https://github.com/humrochagf/wheke/actions">
    <img src="https://github.com/humrochagf/wheke/workflows/Test%20Suite/badge.svg" alt="Test Suite">
  </a>
  <a href="https://pypi.org/project/wheke">
    <img src="https://img.shields.io/pypi/v/wheke.svg" alt="PyPI - Version">
  </a>
  <a href="https://pypi.org/project/wheke">
    <img src="https://img.shields.io/pypi/pyversions/wheke.svg" alt="PyPI - Python Version">
  </a>
</p>

---

# Introduction

**Wheke** is an opinionated framework to build [FastAPI](https://fastapi.tiangolo.com/) based web apps that are focussed in small scale self-hosted applications and having fun 🎉

## Installation

To install Wheke run:

```shell
pip install wheke
```

Then you need a ASGI web server to serve the FastAPI app created by wheke:

```shell
pip install uvicorn[standard]
```

## Example App

To see how a Wheke app in a single file looks like let's create a `main.py` file and add a route to show a timezone aware clock:

```python title="File: main.py"
from datetime import datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from fastapi import APIRouter, HTTPException, status
from wheke import Pod, Wheke

router = APIRouter()


@router.get("/clock")
def clock(tz: str | None = None) -> dict:
    try:
        if tz:
            zone_info = ZoneInfo(tz)
        else:
            zone_info = None
    except ZoneInfoNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid timezone",
        )

    return {"clock": datetime.now(timezone.utc).astimezone(zone_info)}


my_pod = Pod("my-pod", router=router)

wheke = Wheke()
wheke.add_pod(my_pod)

app = wheke.create_app()
```

To start the server run:

```shell
uvicon main:app --reload
```

Now you can check the app at [http://127.0.0.1:8000](http://127.0.0.1:8000)

![wheke homepage](img/wheke-homepage.png)

And you can also check the created clock endpoint at [http://localhost:8000/clock?tz=America/Montreal](http://localhost:8000/clock?tz=America/Montreal)

You should get a response like this:

```json
{"clock": "2023-12-09T20:55:35.194766-05:00"}
```

Also, as any **FastAPI** apps you have built-in api docs at [http://localhost:8000/docs](http://localhost:8000/docs)
