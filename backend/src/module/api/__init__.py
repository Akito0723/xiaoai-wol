from fastapi import APIRouter

from .program_api import router as program_router
from .config_api import router as config_router
from .log_api import router as log_router
__all__ = "v1"

# API 1.0
v1 = APIRouter(prefix="/v1")
v1.include_router(program_router)
v1.include_router(config_router)
v1.include_router(log_router)
