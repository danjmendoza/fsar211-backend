import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Add app and tests directories to Python path
root_path = Path(__file__).parent.parent
sys.path.append(str(root_path / "app"))
sys.path.append(str(root_path / "tests"))

# Import test settings first to override app settings
import test_settings  # noqa: E402

sys.modules["settings"] = test_settings  # Override app settings

from app.db import Base  # noqa: E402
from app.main import app  # noqa: E402

# Create async engine for testing
test_engine = create_async_engine(
    test_settings.SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    echo=True,
)

# Create async session factory
test_async_session = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True)
async def setup_db() -> AsyncGenerator:
    """Create all tables before each test and drop them after."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """Create an async HTTP client for testing."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
