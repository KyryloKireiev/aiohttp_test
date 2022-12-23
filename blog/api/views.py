import json

import sqlalchemy as sa
from aiohttp import web

from blog.api.schemas import (
    PageQueryParamsSchema,
    SignUpSchema,
    UserListSchema,
    UserSchema,
)
from blog.models import User, current_session, make_session
from blog.utils import generate_hash


@make_session
async def index(request):
    await current_session.execute(sa.select(1))
    return web.Response(text="hello aiohttp")


class UserView(web.View):
    @make_session
    async def get(self, *args, **kwargs):
        query_param = PageQueryParamsSchema().load(self.request.query)
        page = query_param["page"]
        count = query_param["count"]
        users = await User.get_all(limit=count, offset=page * count - count)

        return web.Response(
            body=UserListSchema().dumps(
                {
                    "count": len(users),
                    "users": users,
                },
            )
        )


class SignUpView(web.View):
    @make_session
    async def post(self):
        user_data = SignUpSchema().load(await self.request.json())
        username = user_data["username"]
        password = user_data["password"]

        if await User.exists(username=username):
            return web.Response(
                text=json.dumps({"message": "user with the same name already exists"}),
                status=409,
            )

        new_user = await User.create(
            username=username, password=generate_hash(password)
        )
        return web.Response(body=UserSchema().dumps(new_user), status=201)
