import pytest
from httpx import AsyncClient
from src import create_app
from src.api.auth.models import User
from src.api.auth.crypto import get_password_hash


@pytest.mark.anyio
async def test_all_users():
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        user = {"password": "test", "email": "test1@testmail.com"}
        await User.create(**user)
        response = await client.get("/users")
    assert response.status_code == 200
    assert response.json()[0].get("email") == "test1@testmail.com"


@pytest.mark.anyio
async def test_user():
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        user = {"password": "test", "email": "test@testmail.com"}
        await User.create(**user)
        response = await client.get("/user/1")
    assert response.status_code == 200
    assert response.json().get("email") == "test@testmail.com"


@pytest.mark.anyio
async def test_register():
    data = {"password": "test", "email": "test3@testmail.com"}
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.post("/register", json=data)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_login():
    password_hash = get_password_hash("test")
    user = {"password": password_hash, "email": "test@testmail.com"}
    await User.create(**user)
    data = {"password": "test", "email": "test@testmail.com"}
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.post("/login", json=data)
    assert response.status_code == 200


@pytest.mark.anyio
async def test_redundant_user():
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        user = {"password": "test", "email": "test@testmail.com"}
        await User.create(**user)
        response = await client.get("/user/2")
    assert response.status_code == 404


@pytest.mark.anyio
async def test_register_too_many_fields():
    data = {"password": "test", "email": "test3@testmail.com", "username": "test"}
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.post("/register", json=data)
    assert response.status_code == 422


@pytest.mark.anyio
async def test_register_empty_fields():
    data = {"password": "", "email": ""}
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.post("/register", json=data)
    assert response.status_code == 400


@pytest.mark.anyio
async def test_login_wrong_credentials():
    user = {"password": "test", "email": "test@testmail.com"}
    await User.create(**user)
    data = {"password": "wrong", "email": "wrong@email.com"}
    async with AsyncClient(app=create_app(), base_url="http://test") as client:
        response = await client.post("/login", json=data)
    assert response.status_code == 404
