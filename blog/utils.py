import bcrypt
from yarl import URL


def generate_hash(password):
    password_bin = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode("utf-8")


def make_slice_queryset(page, count, queryset):
    start = (page - 1) * count
    stop = (page - 1) * count + count
    return queryset[start:stop:]


def make_previous_page_url(current_url, page):
    if page == 1:
        return None
    previous_url = str(current_url).replace(f"page={page}", f"page={page - 1}")
    return URL(previous_url)


def make_next_page_url(current_url, page, query, query_slice):
    if query[-1] == query_slice[-1]:
        return None
    next_url = str(current_url).replace(f"page={page}", f"page={page + 1}")
    return URL(next_url)
