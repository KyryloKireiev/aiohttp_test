from contextvars import ContextVar

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()

Session = sessionmaker(class_=AsyncSession)

current_session = ContextVar("session")


def make_session(function):
    async def wrapper(*args, **kwargs):
        async with Session() as session:
            async with session.begin():
                token = current_session.set(session)
                result = await function(*args, **kwargs)
                current_session.reset(token)
                return result

    return wrapper


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)

    @classmethod
    async def exists(cls, **kwargs):
        qs = select(cls).filter_by(**kwargs).exists().select()
        return (await current_session.get().execute(qs)).scalar()

    @classmethod
    async def create(cls, **kwargs):
        new_object = cls(**kwargs)
        current_session.get().add(new_object)
        await current_session.get().flush()
        await current_session.get().refresh(new_object)
        return new_object


class CreatedMixin:
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )


class Article(CreatedMixin, BaseModel):
    __tablename__ = "article"

    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    author = Column(Integer, ForeignKey("user.id"))


class Category(BaseModel):
    __tablename__ = "category"

    title = Column(String(100), nullable=False)


class User(CreatedMixin, BaseModel):
    __tablename__ = "user"

    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(128), nullable=False)
