import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_read_root(async_client: AsyncClient) -> None:
    """Test the root endpoint returns the expected greeting."""
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "Welcome to the 211."}
