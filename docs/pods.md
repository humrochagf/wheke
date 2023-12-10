# Pods

The core of Wheke's modularity lies on the `Pod` class.

Once you have your code ready you can bundle it in a Pod to be plugged in Wheke:

```python hl_lines="12 15"
from fastapi import APIRouter
from wheke import Pod, Wheke

router = APIRouter()


@router.get("/hello")
def hello() -> dict:
    return {"hello": "world"}


my_pod = Pod("my-pod", router=router)  # Create the pod

wheke = Wheke()
wheke.add_pod(my_pod)  # Add the pod to wheke

app = wheke.create_app()
```

## Ready to use Pods

Pods can be developed and published as a package for other to use.

These are examples of pods that offer ready to use functionalities:

- [wheke-auth](https://github.com/humrochagf/wheke-auth): A Pod that adds auth to Wheke.
