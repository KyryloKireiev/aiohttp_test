import json

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.future import select

from .models import Session, User
from .security import generate_password_hash


def session_decorator(function):
    async def wrapper(*args, **kwargs):
        async with Session() as session:
            async with session.begin():
                return function(session, *args, **kwargs)

    return wrapper


async def sess():
    async with Session() as session:
        async with session.begin():
            return session


async def index(request):
    async with Session() as session:
        async with session.begin():
            await session.execute(sa.select(1))
    return web.Response(text="hello aiohttp")


async def sign_up(request):
    try:
        data = await request.json()
        user = data.get("username")
        password = data.get("password")
        response_obj = {
            "status": "success",
            "message": "new user created",
            "username": user,
        }

        async with Session() as session:
            async with session.begin():
                session.add_all(
                    [User(username=user, password=generate_password_hash(password))]
                )
            await session.commit()

        return web.Response(text=json.dumps(response_obj), status=201)
    except Exception as exc:
        data = await request.json()
        print(data)
        response_obj = {"status": "failed", "message": str(exc)}
        return web.Response(text=json.dumps(response_obj), status=409)


"""
async def users_list(request):
    async with Session() as session:
        async with session.begin():
            query = select(User)
            cursor = await session.execute(query)
            users = cursor.scalars().all()

            result = [row_to_dict(elem) for elem in users]

    return web.Response(text=json.dumps(result), status=200)
"""


@session_decorator
async def users_list(session, request):
    query = select(User)
    cursor = await session.execute(query)
    users = cursor.scalars().all()

    result = [row_to_dict(elem) for elem in users]

    return web.Response(text=json.dumps(result), status=200)


def row_to_dict(row):
    dct = {}
    for column in row.__table__.columns:
        dct[column.name] = str(getattr(row, column.name))
    return dct
