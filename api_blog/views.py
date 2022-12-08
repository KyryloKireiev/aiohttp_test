import sqlalchemy as sa
from aiohttp import web

from .models import Session


async def index(request):
    async with Session() as session:
        async with session.begin():
            qs = sa.select(1)
            print(await session.execute(qs))
    return web.Response(text="hello aiohttp")
