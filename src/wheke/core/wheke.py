from importlib import import_module

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typer import Typer

from wheke.core.cli import cli
from wheke.core.pod import Pod
from wheke.core.service import ServiceRegistry
from wheke.core.settings import settings


class Wheke:
    pods: list[Pod]

    def __init__(self) -> None:
        self.pods = []

    def create_app(self) -> FastAPI:
        app = FastAPI(title=settings.project_name)

        for pod_full_name in settings.pods:
            module_name, pod_name = pod_full_name.rsplit(".", 1)
            pod: Pod = getattr(import_module(module_name), pod_name)

            for service_type, service_factory in pod.services:
                ServiceRegistry.register(service_type, service_factory)

            if pod.static_url is not None and pod.static_folder is not None:
                app.mount(
                    pod.static_url,
                    StaticFiles(directory=pod.root_path / pod.static_folder),
                    name=f"{pod.name}_static",
                )

            if pod.router:
                app.include_router(pod.router)

            self.pods.append(pod)

        return app

    def create_cli(self) -> Typer:
        for pod_full_name in settings.pods:
            module_name, pod_name = pod_full_name.rsplit(".", 1)
            pod: Pod = getattr(import_module(module_name), pod_name)

            for service_type, service_factory in pod.services:
                ServiceRegistry.register(service_type, service_factory)

            if pod.cli:
                cli.add_typer(pod.cli, name=pod.name)

            self.pods.append(pod)

        return cli
