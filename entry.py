from aiohttp import web
from api_demo.routes import setup_routes


app = web.Application()
setup_routes(app)
web.run_app(app)
