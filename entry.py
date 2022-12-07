from aiohttp.web import run_app

from api_demo.app import create_app, get_config

if __name__ == "__main__":
    app = create_app()
    run_app(
        app,
        host=get_config().get("postgres", {}).get("host"),
        port=get_config().get("postgres", {}).get("port"),
    )
