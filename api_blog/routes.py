from .views import index, sign_up, users_list


def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_get("/users_list/", users_list)
    app.router.add_post("/sign_up/", sign_up)
