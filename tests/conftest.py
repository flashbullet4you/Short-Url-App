from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.database.models import Base
from src.main import app, get_session

engine = create_async_engine(url="sqlite+aiosqlite:///./test.db")

new_session = async_sessionmaker(bind=engine, expire_on_commit=False)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with new_session() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest.fixture(scope="session", autouse=True)
async def setup_db():  # type: ignore
    """
    Фикстура для настройки тестовой базы данных перед запуском тестов.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="function")
async def session():  # type: ignore
    """
    Фикстура для создания и очистки тестовой сессии базы данных перед каждым тестом.
    """
    async with new_session() as session:
        yield session


@pytest.fixture(scope="session")  # type: ignore[untyped-decorator]
async def ac() -> AsyncGenerator[AsyncClient, None]:
    """
    Фикстура для создания AsyncClient для взаимодействия с приложением в тестах.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://testserver"
    ) as ac:
        yield ac
