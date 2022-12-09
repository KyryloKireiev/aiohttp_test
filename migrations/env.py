import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine

from api_blog.app import get_config
from api_blog.models import Base

ALEMBIC_URL = get_config()["db_url"]

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

config.set_main_option("sqlalchemy.url", ALEMBIC_URL)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support


target_metadata = Base.metadata

# target_metadata = None

# other values from the config, defined by the needs of env.py,
# can be acquired:
my_important_option = config.get_main_option("my_important_option")
# ... etc.

engine = create_async_engine(url=ALEMBIC_URL, future=True, echo=True)


async def run_migrations():
    def do_migrations(connection):
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()

    async with engine.connect() as connection:
        await connection.run_sync(do_migrations)

    await engine.dispose()


asyncio.run(run_migrations())

"""
def run_migrations_offline() -> None:

    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:

    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

"""
