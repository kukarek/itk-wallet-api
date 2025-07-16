import asyncio
import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.core.dependencies import get_db
from src.models.db_models import Base
from main import app

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine_test = create_async_engine(DATABASE_URL, echo=False)
TestSessionLocal = sessionmaker(engine_test, expire_on_commit=False, class_=AsyncSession)

@pytest_asyncio.fixture(scope="session", autouse=True)
async def prepare_database():
    # Создание таблиц перед всеми тестами
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Очистка после всех тестов
    await engine_test.dispose()
    if os.path.exists("test.db"):
        os.remove("test.db")

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()