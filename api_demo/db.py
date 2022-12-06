import aiopg.sa

from sqlalchemy import (
    MetaData, Table, Column, ForeignKey,
    Integer, String, DateTime, Text
)

from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Article(Base):
    __tablename__ = 'article'
    id = Column(Integer, primary_key=True)
    article_name = Column(String(200), nullable=False)
    article_text = Column(Text, nullable=False)
    likes = Column(Integer, default="0", nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)
    pub_date = Column(DateTime, nullable=False)


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
