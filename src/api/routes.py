from fastapi import APIRouter

from src.api.v1 import smoke

api_router = APIRouter()
api_router.include_router(smoke.router, prefix="/smoke", tags=["Smoke"])
