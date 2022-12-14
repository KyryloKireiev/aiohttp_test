from .views import UserRegister, UserView, index


def setup_routes(app):
    app.router.add_get("/", index)
    app.router.add_view("/users/", UserView)
    app.router.add_view("/sign-up/", UserRegister)
