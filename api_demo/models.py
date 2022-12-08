from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BaseModel(Base):
    id = Column(Integer, primary_key=True)


class Article(BaseModel):
    __tablename__ = "article"
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Category(BaseModel):
    __tablename__ = "category"
    title = Column(String(100), nullable=False)
