import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.user.models import User


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient, setup_db: AsyncSession) -> None:
    """Test creating a new user."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "resource_type": "volunteer",
    }
    response = await async_client.post(
        "/api/v1/user",
        json=user_data,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["resource_type"] == user_data["resource_type"]

    # Verify in database
    user = await setup_db.get(User, data["id"])
    assert user is not None
    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert user.resource_type == user_data["resource_type"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient, setup_db: AsyncSession) -> None:
    """Test retrieving a user."""
    # Create a test user directly in the database
    user = User(
        name="Get Test User", email="get_test@example.com", resource_type="volunteer"
    )
    setup_db.add(user)
    await setup_db.commit()
    await setup_db.refresh(user)

    # Get the user through API
    response = await async_client.get(f"/api/v1/user/{user.id}")
    print(f"Response: {response.status_code} - {response.json()}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user.name
    assert data["email"] == user.email
    assert data["resource_type"] == user.resource_type


@pytest.mark.asyncio
async def test_list_users(async_client: AsyncClient, setup_db: AsyncSession) -> None:
    """Test listing all users."""
    # Create test users directly in the database
    users = [
        User(
            name="List Test User 1",
            email="list_test1@example.com",
            resource_type="volunteer",
        ),
        User(
            name="List Test User 2",
            email="list_test2@example.com",
            resource_type="volunteer",
        ),
    ]

    for user in users:
        setup_db.add(user)
    await setup_db.commit()

    # List users through API
    response = await async_client.get("/api/v1/user")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "items" in data
    assert "count" in data
    assert len(data["items"]) >= 2  # There might be other users from previous tests
    assert data["count"] >= 2

    # Verify specific users are in the list
    user_emails = [u["email"] for u in data["items"]]
    assert "list_test1@example.com" in user_emails
    assert "list_test2@example.com" in user_emails
