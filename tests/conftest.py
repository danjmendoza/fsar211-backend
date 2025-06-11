import asyncio
import sys
from pathlib import Path
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy import text
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

# Import models first to register them with Base.metadata
from app.db import Base  # noqa: E402
from app.main import app  # noqa: E402

# Create async engine for testing
test_engine = create_async_engine(
    test_settings.SQLALCHEMY_DATABASE_URL,
    poolclass=StaticPool,
    echo=True,
)

# Create async session factory
async_session = sessionmaker(
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
async def setup_db() -> AsyncGenerator[AsyncSession, None]:
    # Drop and recreate all tables
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # Create extension after tables
        await conn.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'))

    # Return session for testing
    async with async_session() as session:
        yield session
        # Rollback any pending changes
        await session.rollback()
        await session.close()


@pytest.fixture
async def async_client(setup_db: AsyncSession) -> AsyncClient:
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
