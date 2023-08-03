import click
import asyncio
from typing import Any
from uvicorn import Config, Server

from cdiapi import settings
from cdiapi.app import create_app
from cdiapi.logs import configure_logging, get_logger


log = get_logger("cdiapi")


async def update_registry()  -> None:
    pass


@click.group(help="Common Data Index API server")
def cli() -> None:
    pass


@cli.command("serve", help="Run uvicorn and serve requests")
def serve() -> None:
    app = create_app()
    server = Server(
        Config(
            app,
            host="0.0.0.0",
            port=settings.PORT,
            proxy_headers=True,
            reload=settings.DEBUG,
            # reload_dirs=[code_dir],
            # debug=settings.DEBUG,
            log_level=settings.LOG_LEVEL,
            server_header=False,
        ),
    )
    configure_logging()
    server.run()


@cli.command("registry-update", help="Re-index the data if newer data is available")
@click.option("-f", "--force", is_flag=True, default=False)
def registry_update(force: bool) -> None:
    configure_logging()
    asyncio.run(update_registry(force=force))


async def _clear_registry() -> None:
    pass
#    es = await get_es()
#    indices: Any = await es.cat.indices(format="json")
#    for index in indices:
#        index_name: str = index.get("index")
#        log.info("Delete index", index=index_name)
#        await es.indices.delete(index=index_name)
#    await es.close()


@cli.command("registry-clear", help="Delete everything in Registry")
def registry_clear() -> None:
    configure_logging()
    asyncio.run(_clear_registry())


if __name__ == "__main__":
    cli()
