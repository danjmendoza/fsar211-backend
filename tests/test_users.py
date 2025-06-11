import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_user(async_client: AsyncClient) -> None:
    """Test creating a new user."""
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "resource_type": "volunteer",
    }
    response = await async_client.post("/api/v1/user", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]
    assert data["resource_type"] == user_data["resource_type"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_get_user(async_client: AsyncClient) -> None:
    """Test retrieving a user."""
    # First create a user
    user_data = {
        "name": "Get Test User",
        "email": "get_test@example.com",
        "resource_type": "volunteer",
    }
    create_response = await async_client.post("/api/v1/user", json=user_data)
    created_user = create_response.json()

    # Now try to get the user
    response = await async_client.get(f"/api/v1/user/{created_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == user_data["name"]
    assert data["email"] == user_data["email"]


@pytest.mark.asyncio
async def test_list_users(async_client: AsyncClient) -> None:
    """Test listing all users."""
    # Create a couple of users
    users = [
        {"name": "User 1", "email": "user1@example.com", "resource_type": "volunteer"},
        {"name": "User 2", "email": "user2@example.com", "resource_type": "volunteer"},
    ]
    for user in users:
        await async_client.post("/api/v1/user", json=user)

    # Get the list of users
    response = await async_client.get("/api/v1/user")
    assert response.status_code == 200
    data = response.json()
    assert "users" in data
    assert len(data["users"]) >= 2  # At least our 2 users should be there
