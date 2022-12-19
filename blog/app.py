import pathlib

import aioreloader
import yaml
from aiohttp.web_app import Application
from sqlalchemy.ext.asyncio import create_async_engine

from blog.middlewares import setup_middlewares
from blog.models import Session
from blog.routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config.yaml"
local_config_path = BASE_DIR / "local.yaml"


def get_config():
    with open(config_path) as base, open(local_config_path) as local:
        config = yaml.safe_load(base)
        local = yaml.safe_load(local)
        config.update(local)
        return config


async def create_app(config):
    app = Application()
    aioreloader.start()
    setup_routes(app)
    setup_middlewares(app)
    app["config"] = config
    app.cleanup_ctx.append(pg_context)
    return app


async def pg_context(app):
    url = app["config"]["db_url"]
    Session.configure(bind=create_async_engine(url, echo=True))
    yield

    await Session.kw["bind"].dispose()
