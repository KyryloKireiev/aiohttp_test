from .views import index, get_categories, get_articles


def setup_routes(app):
    app.router.add_get('/', index)
    app.router.add_get("/cats_list/", get_categories)
    app.router.add_get("/articles_list/", get_articles)

