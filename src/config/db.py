import os
from tortoise.contrib.fastapi import register_tortoise
from src.core.config import settings

match os.environ.get("ENV"):
    case "PRODUCTION":
        db_url = settings.POSTGRES_HEROKU
    case "DEVELOP":
        db_url = (
            f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@"
            f"{settings.POSTGRES_SERVER}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
    case _:
        db_url = "sqlite://:memory:"

DB_CONFIG = {
    "connections": {"default": db_url},
    "apps": {
        "models": {
            "models": ["aerich.models", "src.api.auth.models"],
            "default_connection": "default",
        }
    },
}


def init_tortoise(app: any) -> None:
    register_tortoise(
        app,
        db_url=DB_CONFIG["connections"].get("default"),
        modules={"models": DB_CONFIG["apps"]["models"].get("models")},
        generate_schemas=True,
        add_exception_handlers=True,
    )
