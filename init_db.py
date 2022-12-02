from sqlalchemy import create_engine, MetaData

from api_demo.settings import config
from api_demo.db import category, article
from datetime import datetime

DSN = "postgresql://{user}:{password}@{host}:{port}/{database}"


def create_tables(engine):
    meta = MetaData()
    meta.create_all(bind=engine, tables=[category, article])


def sample_data(engine):
    conn = engine.connect()
    conn.execute(category.insert(), [
        {'category_name': 'Cats',
         'pub_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {'category_name': 'Dogs',
         'pub_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
        {'category_name': 'Mobile phones',
         'pub_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
    ])
    conn.execute(article.insert(), [
        {'article_name': 'Maine coon',
         'article_text': "Some text about maine coon",
         'likes': 0,
         'category_id': 1},
        {'article_name': 'Street cat',
         'article_text': "Some text about street cat",
         'likes': 0,
         'category_id': 1},
        {'article_name': 'Labrador',
         'article_text': "Good dog",
         'likes': 0,
         'category_id': 2},
        {'article_name': "Nokia n97",
         'article_text': "My old phone",
         'likes': 0,
         'category_id': 3},
        {'article_name': 'Iphone 8',
         'article_text': "Some text about iphone 8",
         'likes': 0,
         'category_id': 3},

    ])
    conn.close()


if __name__ == '__main__':
    db_url = DSN.format(**config['postgres'])
    engine = create_engine(db_url)

    create_tables(engine)
    sample_data(engine)
