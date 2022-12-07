import pathlib
import aioreloader

import yaml
from aiohttp.web_app import Application

from api_demo.routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config.yaml'


def get_config():
    with open(config_path) as f:
        return yaml.safe_load(f)


async def create_app():
    app = Application()
    aioreloader.start()
    app["config"] = get_config()
    setup_routes(app)
    return app
