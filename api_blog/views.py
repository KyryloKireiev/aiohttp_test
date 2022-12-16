import json

import sqlalchemy as sa
from aiohttp import web
from marshmallow import ValidationError
from sqlalchemy.future import select

from .models import Session, User
from .schemas import SignUpSchema
from .security import generate_password_hash


def session_decorator(function):
    async def wrapper(*args, **kwargs):
        async with Session() as session:
            async with session.begin():
                print(session, *args, **kwargs)
                return await function(*args, session=session, **kwargs)

    return wrapper


def row_to_dict(row):
    dct = {}
    for column in row.__table__.columns:
        dct[column.name] = str(getattr(row, column.name))
    return dct


@session_decorator
async def index(request, session):
    await session.execute(sa.select(1))
    return web.Response(text="hello aiohttp")


class UserView(web.View):
    @session_decorator
    async def get(self, *args, session, **kwargs):
        query = select(User)
        cursor = await session.execute(query)
        users = cursor.scalars().all()

        result = [row_to_dict(elem) for elem in users]

        return web.Response(text=json.dumps(result), status=200)


class SignUpView(web.View):
    async def post(self):
        try:
            request = self.request
            user_data = await request.json()
            schema = SignUpSchema()
            user_is_valid = schema.load(user_data)
            result = schema.dump(user_is_valid)
            user = result["username"]
            password = result["password"]
            response_obj = {
                "status": "success",
                "message": "new user created",
                "username": user,
            }
        except ValidationError as exp:
            response_obj = {
                "status": "failed",
                "message": str(exp),
            }
            return web.Response(text=json.dumps(response_obj), status=422)

        async with Session() as session:
            async with session.begin():
                exist = select(User).where(User.username == user)
                result = await session.execute(exist)
                user_in_db = result.scalars().all()
                if user_in_db:
                    response_obj = {
                        "status": "failed",
                        "message": "user with the same name already exists",
                    }
                    return web.Response(text=json.dumps(response_obj), status=409)

                session.add(
                    User(username=user, password=generate_password_hash(password))
                )

            return web.Response(text=json.dumps(response_obj), status=201)
