import asyncio
import os
from collections.abc import AsyncIterator, Iterator
from pathlib import Path

import asyncpg
import pytest
import pytest_asyncio
from alembic import command
from alembic.config import Config
from httpx import ASGITransport, AsyncClient
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config.settings import Settings

development_url = make_url(Settings().database_url)
TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    development_url.set(database="ccdip_test").render_as_string(hide_password=False),
)
os.environ["DATABASE_URL"] = TEST_DATABASE_URL


async def _recreate_test_database() -> None:
    url = make_url(TEST_DATABASE_URL)
    connection = await asyncpg.connect(
        user=url.username,
        password=url.password,
        host=url.host,
        port=url.port,
        database="postgres",
    )
    try:
        database = url.database
        await connection.execute(
            "SELECT pg_terminate_backend(pid) FROM pg_stat_activity "
            "WHERE datname = $1 AND pid <> pg_backend_pid()",
            database,
        )
        await connection.execute(f'DROP DATABASE IF EXISTS "{database}"')
        await connection.execute(f'CREATE DATABASE "{database}"')
    finally:
        await connection.close()


@pytest.fixture(scope="session", autouse=True)
def migrated_database() -> Iterator[None]:
    asyncio.run(_recreate_test_database())
    config = Config(str(Path(__file__).parents[1] / "alembic.ini"))
    command.upgrade(config, "head")
    yield


@pytest_asyncio.fixture
async def db_session(migrated_database: None) -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(TEST_DATABASE_URL)
    connection = await engine.connect()
    transaction = await connection.begin()
    factory = async_sessionmaker(bind=connection, expire_on_commit=False)
    async with factory() as session:
        yield session
    await transaction.rollback()
    await connection.close()
    await engine.dispose()


@pytest_asyncio.fixture
async def client(
    db_session: AsyncSession,
) -> AsyncIterator[AsyncClient]:
    from app.db.session import get_session
    from app.main import app

    async def override_session() -> AsyncIterator[AsyncSession]:
        yield db_session

    app.dependency_overrides[get_session] = override_session
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as test_client:
        yield test_client
    app.dependency_overrides.clear()
