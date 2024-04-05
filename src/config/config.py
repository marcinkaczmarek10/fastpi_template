import os
from pydantic import BaseSettings, AnyHttpUrl, validator, PostgresDsn
from typing import Union, Optional
from pathlib import Path


class Settings(BaseSettings):
    PROJECT_NAME: str
    SECRET_KEY: str
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, list[str]]) -> Union[list[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: Optional[str]
    POSTGRES_USER: Optional[str]
    POSTGRES_PASSWORD: Optional[str]
    POSTGRES_DB: Optional[str]
    POSTGRES_PORT: Optional[str]
    DATABASE_URI: Optional[PostgresDsn] = None

    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_USERNAME: str
    MAIL_PASSWORD: str

    @classmethod
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, values: dict[str, any], v: Optional[str]) -> any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
            port=values.get("POSTGRES_PORT"),
        )

    BASE_DIR = Path(__file__).resolve().parent.parent
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    UPLOADS_ROOT = os.path.join(MEDIA_ROOT, "uploads")

    class Config:
        case_sensitive = True


match os.environ.get("ENV"):
    case "DEVELOP" | "PRODUCTION":
        print(f"{os.environ.get('ENV')} settings!")
        settings = Settings()
    case _:
        print("Testing settings!")
        settings = Settings(PROJECT_NAME="TESTING", SECRET_KEY="testing")
