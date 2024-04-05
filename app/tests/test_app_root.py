import pytest
from httpx import AsyncClient
from src import create_app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
