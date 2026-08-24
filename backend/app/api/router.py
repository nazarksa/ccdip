from fastapi import APIRouter

from app.api.domain import router as domain_router
from app.api.health import router as health_router

root_router = APIRouter()
root_router.include_router(health_router)

api_router = APIRouter()
api_router.include_router(domain_router)
