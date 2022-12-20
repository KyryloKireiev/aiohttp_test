import json

from aiohttp import web
from marshmallow import ValidationError


def create_error_middleware():
    @web.middleware
    async def error_middleware(request, handler):
        try:
            return await handler(request)

        except web.HTTPException as ex:
            response_obj = {"error": str(ex.text)}
            return web.Response(text=json.dumps(response_obj))

        except ValidationError as ex:
            response_obj = {"error": str(ex)}
            return web.Response(text=json.dumps(response_obj))

    return error_middleware


def setup_middlewares(app):
    error_middleware = create_error_middleware()
    app.middlewares.append(error_middleware)
