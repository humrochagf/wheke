from wheke import (
    Wheke,
    demo_pod,
)

from .pods import test_pod


def make_wheke() -> Wheke:
    wheke = Wheke()
    wheke.add_pod(demo_pod)
    wheke.add_pod(test_pod)

    return wheke
