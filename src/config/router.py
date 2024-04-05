from fastapi import APIRouter
from src.api.api_router import api_router


router = APIRouter()
router.include_router(api_router)
