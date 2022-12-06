import json
from aiohttp import web


async def index(request):
    return web.Response(text=json.dumps({"text": "Hello Aiohttp!"}), status=200)

