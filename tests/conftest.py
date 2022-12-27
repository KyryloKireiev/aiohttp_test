import pytest_asyncio
import yaml
from sqlalchemy.ext.asyncio import create_async_engine

from blog.app import BASE_DIR, create_app
from blog.models import Base, Session


async def db_action(url, method) -> None:
    async with Session(bind=create_async_engine(url)) as session:
        async with session.bind.begin() as conn:
            await conn.run_sync(getattr(Base.metadata, method))


@pytest_asyncio.fixture
def test_config():
    test_config_path = BASE_DIR / "tests" / "test_config.yaml"
    with open(test_config_path) as test:
        config = yaml.safe_load(test)
        return config


@pytest_asyncio.fixture
async def test_client(aiohttp_client, test_config):
    print("hello")
    app = await create_app(config=test_config)
    try:
        await db_action(url=test_config["db_url"], method="create_all")
        yield await aiohttp_client(app)
    finally:
        await db_action(url=test_config["db_url"], method="drop_all")
