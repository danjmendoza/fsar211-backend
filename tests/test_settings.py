"""Test settings for the FastAPI application."""

# Database settings
PG_HOST = "test-db"  # Use container name from Docker network
PG_PORT = "5432"
PG_USER = "test"
PG_PASSWORD = "test"
PG_DB = "test"

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URL = (
    f"postgresql+asyncpg://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}"
)
SQLALCHEMY_ECHO = False
