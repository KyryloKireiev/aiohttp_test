import aiopg.sa

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, Date
)

__all__ = ['category', 'article']

meta = MetaData()

category = Table(
    'category', meta,

    Column('id', Integer, primary_key=True),
    Column('category_name', String(100), nullable=False),
    Column('pub_date', Date, nullable=False)
)

article = Table(
    'article', meta,

    Column('id', Integer, primary_key=True),
    Column('article_name', String(100), nullable=False),
    Column('article_text', String(1000), nullable=False),
    Column('likes', Integer, server_default="0", nullable=False),

    Column('category_id',
           Integer,
           ForeignKey('category.id', ondelete='CASCADE'))
)


async def pg_context(app):
    conf = app['config']['postgres']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

    yield

    app['db'].close()
    await app['db'].wait_closed()
