import pathlib

import aiopg.sa
import yaml
from aiohttp.web_app import Application

from api_demo.routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config.yaml'


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()


def get_config():
    with open(config_path) as f:
        return yaml.safe_load(f)


async def create_app():
    app = Application()
    app["config"] = get_config()
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    return app
