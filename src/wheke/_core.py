from importlib import import_module

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from typer import Typer

from ._cli import empty_callback, version
from ._pod import Pod
from ._service import get_service_registry
from ._settings import WhekeSettings, get_settings


class Wheke:
    """
    The Wheke class is the entry point to build an application.
    """

    pods: list[Pod]
    "The list of pods plugged to Wheke."

    def __init__(
        self, settings: WhekeSettings | type[WhekeSettings] | None = None
    ) -> None:
        self.pods = []

        if settings is None:
            settings_cls = WhekeSettings
            settings_obj = WhekeSettings()
        elif isinstance(settings, WhekeSettings):
            settings_cls = type(settings)
            settings_obj = settings
        else:
            settings_cls = settings
            settings_obj = settings_cls()

        get_service_registry().register_value(settings_cls, settings_obj)

        if settings_cls != WhekeSettings:
            get_service_registry().register_value(WhekeSettings, settings_obj)

        for pod in get_settings(WhekeSettings).pods:
            self.add_pod(pod)

    def add_pod(self, pod_to_add: Pod | str) -> None:
        """
        Programatically plug a `Pod` into Wheke.
        """
        pod: Pod

        if isinstance(pod_to_add, str):
            module_name, pod_name = pod_to_add.rsplit(".", 1)
            pod = getattr(import_module(module_name), pod_name)
        else:
            pod = pod_to_add

        for service_type, service_factory in pod.services:
            get_service_registry().register_factory(service_type, service_factory)

        self.pods.append(pod)

    def create_app(self) -> FastAPI:
        """
        Create a FastAPI app with all plugged pods.
        """
        app = FastAPI(title=get_settings(WhekeSettings).project_name)

        for pod in self.pods:
            if pod.static_url is not None and pod.static_path is not None:
                app.mount(
                    pod.static_url,
                    StaticFiles(directory=pod.static_path),
                    name=f"{pod.name}_static",
                )

            if pod.router:
                app.include_router(pod.router)

        return app

    def create_cli(self) -> Typer:
        """
        Create a Typer cli with all plugged pods.
        """
        cli = Typer(no_args_is_help=True)
        cli.callback()(empty_callback)
        cli.command("version", help="Show Wheke version")(version)

        for pod in self.pods:
            if pod.cli:
                cli.add_typer(pod.cli, name=pod.name)

        return cli
