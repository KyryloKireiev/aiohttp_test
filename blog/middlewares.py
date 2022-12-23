import json

from aiohttp import web
from marshmallow import ValidationError


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except ValidationError as ex:
        response_obj = {"error": str(ex)}
        return web.Response(text=json.dumps(response_obj))


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
