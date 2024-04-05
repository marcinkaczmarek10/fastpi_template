import pytest
import asyncio
from tortoise import Tortoise

DB_URL = "sqlite://:memory:"


async def init_db(db_url: str, create_db: bool = False, schemas: bool = False):
    await Tortoise.init(
        db_url=db_url, modules={"models": ["src.api.auth.models"]}, _create_db=create_db
    )
    if schemas:
        await Tortoise.generate_schemas()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest.fixture(autouse=True)
async def init_tests():
    await init_db(db_url=DB_URL, create_db=True, schemas=True)
    yield
    await Tortoise._drop_databases()
