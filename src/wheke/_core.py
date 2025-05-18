from collections.abc import AsyncGenerator
from importlib import import_module
from typing import Any

from click import get_current_context
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from svcs import Container, Registry
from svcs.fastapi import lifespan as svcs_lifespan
from typer import Context, Typer

from wheke._constants import KEY_CONTAINER, KEY_REGISTRY

from ._cli import version
from ._pod import Pod
from ._settings import WhekeSettings


class Wheke:
    """
    The Wheke class is the entry point to build an application.
    """

    settings_cls: type[WhekeSettings]
    "The loaded settings class."

    settings: WhekeSettings
    "The loaded settings object."

    pods: list[Pod]
    "The list of pods plugged to Wheke."

    def __init__(
        self, settings: WhekeSettings | type[WhekeSettings] | None = None
    ) -> None:
        self.pods = []

        if settings is None:
            self.settings_cls = WhekeSettings
            self.settings = WhekeSettings()
        elif isinstance(settings, WhekeSettings):
            self.settings_cls = type(settings)
            self.settings = settings
        else:
            self.settings_cls = settings
            self.settings = settings()

        for pod in self.settings.pods:
            self.add_pod(pod)

    def setup_registry(self, registry: Registry) -> None:
        """
        Populates the registry with all redistered pods services.
        """
        registry.register_value(self.settings_cls, self.settings)

        if self.settings_cls != WhekeSettings:
            registry.register_value(WhekeSettings, self.settings)

        for pod in self.pods:
            for config in pod.services:
                if config.as_value:
                    with Container(registry) as container:
                        service = config.service_factory(container)

                    registry.register_value(
                        config.service_type,
                        service,
                        ping=config.health_check,
                        on_registry_close=config.cleanup,
                    )
                else:
                    registry.register_factory(
                        config.service_type,
                        config.service_factory,
                        ping=config.health_check,
                        on_registry_close=config.cleanup,
                    )

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

        self.pods.append(pod)

    def create_app(self) -> FastAPI:
        """
        Create a FastAPI app with all plugged pods.
        """

        @svcs_lifespan
        async def lifespan(
            _: FastAPI, registry: Registry
        ) -> AsyncGenerator[dict[str, object], None]:
            self.setup_registry(registry)
            yield {}

        app = FastAPI(title=self.settings.project_name, lifespan=lifespan)

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

        def registry_callback(ctx: Context) -> None:
            registry = Registry()
            self.setup_registry(registry)

            ctx.ensure_object(dict)
            ctx.obj[KEY_REGISTRY] = registry
            ctx.obj[KEY_CONTAINER] = Container(registry)

        def cleanup_callback(_: Any) -> None:
            ctx = get_current_context()
            ctx.ensure_object(dict)
            ctx.obj[KEY_CONTAINER].close()
            del ctx.obj[KEY_CONTAINER]
            ctx.obj[KEY_REGISTRY].close()
            del ctx.obj[KEY_REGISTRY]

        cli = Typer(no_args_is_help=True)
        cli.callback(result_callback=cleanup_callback)(registry_callback)
        cli.command("version", help="Show Wheke version")(version)

        for pod in self.pods:
            if pod.cli:
                cli.add_typer(pod.cli, name=pod.name)

        return cli
