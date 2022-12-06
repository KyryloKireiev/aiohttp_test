from sqlalchemy import ( Column, ForeignKey,
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

