"""Alembic async (asyncpg). DATABASE_URL manda sobre alembic.ini."""

import asyncio
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy.ext.asyncio import async_engine_from_config

# ponytail: backend/ al path para `import src...` funcione desde cualquier cwd
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

if db_url := os.getenv("DATABASE_URL"):
    config.set_main_option("sqlalchemy.url", db_url)

import src.db.models  # noqa: E402,F401  -- registra Item en Base.metadata
from src.db.database import Base  # noqa: E402

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    engine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=None,
    )
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()


asyncio.run(run_migrations_online())
