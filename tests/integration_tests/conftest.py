import asyncio
import sys

# if sys.platform == "win32":
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import os
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import NullPool
from dotenv import load_dotenv
os.environ["PGGSSLIB"] = "disable"

load_dotenv(".env.test")
from app.database import Base
from app.dependency import get_db
from app.models import Card, Operation, User
from main import app



TEST_DATABASE_URL = os.environ["TEST_DATABASE_URL"]


# @pytest_asyncio.fixture(scope="session")
# async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
#     """Створює глобальний AsyncEngine."""
#     engine = create_async_engine(
#         TEST_DATABASE_URL,
#         connect_args={
#             "ssl": False,
#             "gsslib": "sspi",  # Запобігає помилкам SSPI/GSSAPI на Windows
#         },
#         poolclass=NullPool,  # Уникає зависання закритих сокетів у пулі
#     )
#     yield engine
#     await engine.dispose()


@pytest_asyncio.fixture(scope="session")
async def db_engine() -> AsyncGenerator[AsyncEngine, None]:
    # create_engine — наша обёртка над create_async_engine (контекстный менеджер)
    test_engine = create_async_engine(TEST_DATABASE_URL, connect_args={"ssl": False, "gsslib": "sspi"}, poolclass=NullPool)
    yield test_engine
    await test_engine.dispose()
    # async with create_async_engine(TEST_DATABASE_URL) as engine:
    #     async with engine.begin() as conn:
    #         await conn.run_sync(Base.metadata.drop_all)
    #         await conn.run_sync(Base.metadata.create_all)
    #     yield engine  

@pytest_asyncio.fixture(scope="session")
async def session_factory(db_engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )

@pytest_asyncio.fixture
async def db_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncEngine, None]:
    """Створює фабрику асинхронних сесій SQLAlchemy."""
    SessionLocal = async_sessionmaker(
        bind=db_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    async with SessionLocal() as session:
        yield session
    # return async_sessionmaker(
    #     bind=db_engine,
    #     class_=AsyncSession,
    #     expire_on_commit=False,
    #     autoflush=False,
    # )


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_database(db_engine: AsyncEngine):
    """
    Створює всі таблиці на початку тестової сесії через Base.metadata
    та видаляє їх після завершення всіх тестів.
    """
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_app_dependencies(session_factory):
    """Перевизначає залежність FastAPI get_db для використання тестової БД."""
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()


@pytest_asyncio.fixture(autouse=True)
async def clean_database(session_factory):
    """Очищає дані з таблиць перед кожним окремим тестом у правильному порядку FK."""
    async with session_factory() as session:
        async with session.begin():
            await session.execute(delete(Operation))
            await session.execute(delete(Card))
            await session.execute(delete(User))


# @pytest_asyncio.fixture
# async def db_session(session_factory: async_sessionmaker[AsyncSession]) -> AsyncGenerator[AsyncSession, None]:
#     """Фікстура для отримання БД-сесії всередині тесту."""
#     async with session_factory() as session:
#         yield session


@pytest_asyncio.fixture
async def client() -> AsyncGenerator[AsyncClient, None]:
    """Асинхронний HTTP-клієнт для перевірки FastAPI ендпоінтів."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as test_client:
        yield test_client