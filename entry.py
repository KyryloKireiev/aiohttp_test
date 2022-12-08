from aiohttp.web import run_app

from api_demo.app import create_app, get_config

if __name__ == "__main__":
    config = get_config()
    app = create_app(config)
    run_app(
        app,
        host=config["server"]["host"],
        port=config["server"]["port"],
    )
