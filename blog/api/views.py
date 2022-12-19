import json

import sqlalchemy as sa
from aiohttp import web
from sqlalchemy.future import select

from blog.api.schemas import SignUpSchema, UserSchema
from blog.models import User, current_session, make_session


@make_session
async def index(request):
    await current_session.get().execute(sa.select(1))
    return web.Response(text="hello aiohttp")


class UserView(web.View):
    @make_session
    async def get(self, *args, **kwargs):
        query = select(User)
        cursor = await current_session.get().execute(query)
        users = cursor.scalars().all()
        return web.Response(text=UserSchema().dumps(users, many=True), status=200)


class SignUpView(web.View):
    @make_session
    async def post(self):
        user_data = SignUpSchema().load(await self.request.json())
        user = user_data["username"]
        password = user_data["password"]

        if await User.exists(username=user):
            return web.Response(
                text=json.dumps(
                    {
                        "status": "failed",
                        "message": "user with the same name already exists",
                    }
                ),
                status=409,
            )

        new_user = await User.create(username=user, password=password)
        return web.Response(text=UserSchema().dumps(new_user), status=201)
