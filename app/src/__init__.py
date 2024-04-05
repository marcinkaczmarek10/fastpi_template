from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import subprocess
import os
from contextlib import asynccontextmanager
from apscheduler.schedulers.background import BackgroundScheduler

from src.config.config import settings
from src.config.router import router
from src.api.photo.crons import remove_unused_models


def setup_files_directories():
    if not os.path.exists(settings.STATIC_ROOT):
        os.makedirs(settings.STATIC_ROOT)

    if not os.path.exists(settings.MEDIA_ROOT):
        os.makedirs(settings.MEDIA_ROOT)


@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = BackgroundScheduler()
    scheduler.add_job(remove_unused_models, "cron", hour="0", minute="15")
    scheduler.start()
    yield


def create_app() -> FastAPI:
    subprocess.run(["alembic", "upgrade", "head"])

    app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_files_directories()
    app.mount(
        settings.STATIC_ROOT, StaticFiles(directory=settings.STATIC_ROOT), name="static"
    )
    app.include_router(router)

    return app
