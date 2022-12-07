from sqlalchemy import (Column, ForeignKey,
                        Integer, String, DateTime, Text
                        )
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class BaseModel(Base):
    id = Column(Integer, primary_key=True)


class Article(BaseModel):
    __tablename__ = 'article'
    article_name = Column(String(200), nullable=False)
    article_text = Column(Text, nullable=False)
    likes = Column(Integer, default=0, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id', ondelete='CASCADE'))
    create_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    update_at = Column(DateTime(timezone=True), onupdate=func.now())


class Category(BaseModel):
    __tablename__ = 'category'
    category_name = Column(String(100), nullable=False)

