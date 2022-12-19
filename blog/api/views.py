import json

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.future import select

from blog.models import User, current_session, session_decorator
from blog.api.schemas import SignUpSchema
from blog.utils import generate_password_hash


@session_decorator
async def index(request):
    await current_session.get().execute(sa.select(1))
    return web.Response(text="hello aiohttp")


class UserView(web.View):
    @session_decorator
    async def get(self, *args, **kwargs):
        query = select(User)
        cursor = await current_session.get().execute(query)
        users = cursor.scalars().all()
        return web.Response(text=SignUpSchema().dumps(users, many=True), status=200)


class SignUpView(web.View):
    @session_decorator  # todo rename decorator
    async def post(self):
        user_data = SignUpSchema().load(await self.request.json())
        user = user_data["username"]
        password = user_data["password"]

        if await User.exists(username=user):
            return web.Response(text=json.dumps({
                "status": "failed",
                "message": "user with the same name already exists",
            }), status=409)

        # user = await User.create()  todo
        user = current_session.get().get().add(User(username=user, password=generate_password_hash(password)))
        # todo use another scheme in response (id, username)
        return web.Response(text=SignUpSchema().dumps({
                user,
        }), status=201)
