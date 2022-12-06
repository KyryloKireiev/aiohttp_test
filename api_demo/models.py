from sqlalchemy import (Column, ForeignKey,
                        Integer, String, DateTime, Text
                        )

from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class BlogBase(object):
    id = Column(Integer, primary_key=True)
    pub_date = Column(DateTime, default=datetime.utcnow(), nullable=False)


class Article(BlogBase, Base):
    __tablename__ = 'article'
    article_name = Column(String(200), nullable=False)
    article_text = Column(Text, nullable=False)
    likes = Column(Integer, default="0", nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))


class Category(BlogBase, Base):
    __tablename__ = 'category'
    category_name = Column(String(100), nullable=False)

