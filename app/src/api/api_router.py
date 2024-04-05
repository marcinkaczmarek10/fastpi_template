from fastapi import APIRouter
from .auth.routes import auth
from .photo.routes import photo

api_router = APIRouter()
api_router.include_router(auth)
api_router.include_router(photo)


@api_router.get("/")
async def read_root():
    return {"Hello": "World"}
