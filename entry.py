from aiohttp import web
from api_demo.routes import setup_routes
from api_demo.settings import config
from api_demo.db import pg_context


if __name__ == "__main__":
    app = web.Application()
    app["config"] = config
    setup_routes(app)
    app.cleanup_ctx.append(pg_context)
    web.run_app(app)
