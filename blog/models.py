from contextvars import ContextVar
from functools import wraps

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
from sqlalchemy.orm import load_only, sessionmaker
from sqlalchemy.sql import func

Base = declarative_base()


class ContextProxy:
    """Proxy for context variables."""

    def __init__(self, contextvar):
        """Initialize.

        :param contextvar: context variable
        """
        self.var = contextvar
        self.set = self.var.set
        self.reset = self.var.reset

    def __getattr__(self, attr):
        """Get context variable attribute.

        :param attr: attribute
        :return: attribute value or None
        """
        context = self.var.get(None)
        return getattr(context, attr, None)


Session = sessionmaker(class_=AsyncSession)

_current_session = ContextVar("session")
current_session = ContextProxy(_current_session)


def make_session(function):
    @wraps(function)
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
        return (await current_session.execute(qs)).scalar()

    @classmethod
    async def create(cls, **kwargs):
        new_object = cls(**kwargs)
        current_session.add(new_object)
        await current_session.flush()
        await current_session.refresh(new_object)
        return new_object

    @classmethod
    async def get_all(cls, **kwargs):
        query = select(cls)
        cursor = await current_session.execute(query)
        return cursor.scalars().all()


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

    @classmethod
    async def get_all(cls, limit, offset):
        query = (
            select(cls)
            .options(load_only(cls.id, cls.username, cls.created_at))
            .limit(limit)
            .offset(offset)
        )
        cursor = await current_session.execute(query)
        return cursor.scalars().all()
