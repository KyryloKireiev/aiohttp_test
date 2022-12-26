import pytest
import pytest_asyncio
import yaml

from blog.app import BASE_DIR, create_app


@pytest.fixture
def test_config():
    test_config_path = BASE_DIR / "tests" / "test_config.yaml"
    with open(test_config_path) as test:
        config = yaml.safe_load(test)
        return config


@pytest_asyncio.fixture
async def test_client(aiohttp_client, test_config):
    app = await create_app(test_config)
    yield await aiohttp_client(app)
