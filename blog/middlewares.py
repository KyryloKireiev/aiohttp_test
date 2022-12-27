from aiohttp import web
from marshmallow import ValidationError


@web.middleware
async def error_middleware(request, handler):
    try:
        return await handler(request)
    except ValidationError as error:
        return web.Response(text=str(error), status=409)


def setup_middlewares(app):
    app.middlewares.append(error_middleware)
