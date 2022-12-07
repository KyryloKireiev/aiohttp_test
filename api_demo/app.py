import pathlib

import aioreloader
import yaml
from aiohttp.web_app import Application

from api_demo.routes import setup_routes

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / "config.yaml"
local_config_path = BASE_DIR / "local.yaml"


def get_config():
    with open(config_path) as base, open(local_config_path) as local:
        config = yaml.safe_load(base)
        local = yaml.safe_load(local)
        return config.update(local)


async def create_app():
    app = Application()
    aioreloader.start()
    app["config"] = get_config()
    setup_routes(app)
    return app
