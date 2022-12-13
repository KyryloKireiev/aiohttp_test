import sqlalchemy as sa
from aiohttp import web

from .models import Session


async def index(request):
    async with Session() as session:
        async with session.begin():
            await session.execute(sa.select(1))
    return web.Response(text="hello aiohttp")
