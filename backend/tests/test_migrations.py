import asyncio
from pathlib import Path

import asyncpg
from alembic import command
from alembic.config import Config
from sqlalchemy.engine import make_url

from app.config import get_settings

TEST_DATABASE_URL = get_settings().database_url


async def _table_names() -> set[str]:
    url = make_url(TEST_DATABASE_URL)
    connection = await asyncpg.connect(
        user=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database=url.database,
    )
    try:
        rows = await connection.fetch("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
        return {row["tablename"] for row in rows}
    finally:
        await connection.close()


def test_migrations_rebuild_database_from_empty(migrated_database: None) -> None:
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    command.downgrade(config, "base")
    command.upgrade(config, "head")

    tables = asyncio.run(_table_names())

    assert {"organizations", "projects", "activities", "contracts", "documents"} <= tables
