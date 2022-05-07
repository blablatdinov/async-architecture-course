import asyncio
from asyncio.events import AbstractEventLoop
import sys
from typing import Generator, AsyncGenerator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.settings import settings
from app.web.application import get_app
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine, AsyncConnection
from sqlalchemy.orm import sessionmaker
from app.db.dependencies import get_db_session
from app.db.utils import create_database, drop_database

import nest_asyncio

nest_asyncio.apply()

@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """
    Create an instance of event loop for tests.

    This hack is required in order to get `dbsession` fixture to work.
    Because default fixture `event_loop` is function scoped,
    but dbsession requires session scoped `event_loop` fixture.

    :yields: event loop.
    """
    python_version = sys.version_info[:2]
    if sys.platform.startswith("win") and python_version >= (3, 8):
        # Avoid "RuntimeError: Event loop is closed" on Windows when tearing down tests
        # https://github.com/encode/httpx/issues/914
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()
@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def _engine() -> AsyncGenerator[AsyncEngine, None]:
    """
    Create engine and databases.

    :yield: new engine.
    """
    from app.db.meta import meta  # noqa: WPS433
    from app.db.models import load_all_models  # noqa: WPS433

    load_all_models()

    await create_database()

    engine = create_async_engine(str(settings.db_url))
    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    try:
        yield engine
    finally:
        await engine.dispose()
        await drop_database()

@pytest.fixture()
@pytest.mark.asyncio
async def dbsession(_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    """
    Get session to database.

    Fixture that returns a SQLAlchemy session with a SAVEPOINT, and the rollback to it
    after the test completes.

    :param _engine: current engine.
    :yields: async session.
    """
    connection = await _engine.connect()
    trans = await connection.begin()

    session_maker = sessionmaker(
        connection, expire_on_commit=False, class_=AsyncSession,
    )
    session = session_maker()

    try:
        yield session
    finally:
        await session.close()
        await trans.rollback()
        await connection.close()


@pytest.fixture()
@pytest.mark.asyncio
async def transaction(_engine: AsyncEngine) -> AsyncGenerator[AsyncConnection, None]:
    """
    Create and obtain a transaction.

    :param _engine: current database engine.
    :yield: connection.
    """
    conn = await _engine.begin()
    try:
        yield conn
    finally:
        await conn.rollback()




@pytest.fixture()
def fastapi_app(
    dbsession: AsyncSession,

) -> FastAPI:
    """
    Fixture for creating FastAPI app.

    :return: fastapi app with mocked dependencies.
    """
    application = get_app()
    application.dependency_overrides[get_db_session] = lambda: dbsession

    return application  # noqa: WPS331

@pytest.fixture(scope="function")
def client(
    fastapi_app: FastAPI,
) -> TestClient:
    """
    Fixture that creates client for requesting server.

    :param fastapi_app: the application.
    :return: client for the app.
    """
    return TestClient(app=fastapi_app)
