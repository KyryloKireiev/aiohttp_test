from aiohttp import web
from api_demo import db


async def index(request):
    return web.Response(text='Hello Aiohttp!')


async def get_categories(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.category.select())
        records = await cursor.fetchall()
        categories = [dict(q) for q in records]
        return web.Response(text=str(categories))


async def get_articles(request):
    async with request.app['db'].acquire() as conn:
        cursor = await conn.execute(db.article.select())
        records = await cursor.fetchall()
        articles = [dict(q) for q in records]
        return web.Response(text=str(articles))
