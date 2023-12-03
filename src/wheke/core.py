from collections.abc import Generator, Iterable
from importlib import import_module

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typer import Typer

from wheke.cli import empty_callback, version
from wheke.pod import Pod
from wheke.service import ServiceRegistry
from wheke.settings import settings


class Wheke:
    pods: list[Pod]

    def __init__(self) -> None:
        self.pods = []

    def _gen_pods(self) -> Iterable[Pod]:
        for pod_full_name in settings.pods:
            module_name, pod_name = pod_full_name.rsplit(".", 1)
            pod: Pod = getattr(import_module(module_name), pod_name)

            for service_type, service_factory in pod.services:
                ServiceRegistry.register(service_type, service_factory)

            yield pod

    def create_app(self) -> FastAPI:
        app = FastAPI(title=settings.project_name)

        for pod in self._gen_pods():
            if pod.static_url is not None and pod.static_folder is not None:
                app.mount(
                    pod.static_url,
                    StaticFiles(directory=pod.static_folder),
                    name=f"{pod.name}_static",
                )

            if pod.router:
                app.include_router(pod.router)

            self.pods.append(pod)

        return app

    def create_cli(self) -> Typer:
        cli = Typer(no_args_is_help=True)
        cli.callback()(empty_callback)
        cli.command("version", help="Show Wheke version")(version)

        for pod in self._gen_pods():
            if pod.cli:
                cli.add_typer(pod.cli, name=pod.name)

            self.pods.append(pod)

        return cli
