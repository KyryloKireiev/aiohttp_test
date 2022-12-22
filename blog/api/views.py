import json

import sqlalchemy as sa
from aiohttp import web

from blog.api.schemas import (
    SignUpSchema,
    UserListSchema,
    UserQuerySchema,
    UserSchema,
)
from blog.models import User, current_session, make_session
from blog.utils import (
    make_next_page_url,
    make_previous_page_url,
    make_slice_queryset,
)


@make_session
async def index(request):
    await current_session.get().execute(sa.select(1))
    return web.Response(text="hello aiohttp")


class UserView(web.View):
    @make_session
    async def get(self, *args, **kwargs):
        users_query_param = UserQuerySchema().load(self.request.query)
        page = users_query_param["page"]
        count = users_query_param["count"]
        current_url = self.request.url
        query = await User.get_all()
        query_slice = make_slice_queryset(page, count, query)
        return web.Response(
            body=UserListSchema().dumps(
                {
                    "count": len(query_slice),
                    "previous_page": make_previous_page_url(current_url, page),
                    "next_page": make_next_page_url(
                        current_url, page, query, query_slice
                    ),
                    "users": query_slice,
                },
                indent=4,
                sort_keys=True,
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

        new_user = await User.create(username=username, password=password)
        return web.Response(text=UserSchema().dumps(new_user), status=201)
