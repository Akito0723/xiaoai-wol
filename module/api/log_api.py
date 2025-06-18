import logging

from fastapi import APIRouter, Response
from module.conf import LOG_PATH, VERSION, STRING_IO

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/log", tags=["log"])


@router.get("", response_model=str)
async def get_log():
    if VERSION == "DEV_VERSION":
        return Response(STRING_IO.getvalue(), media_type="text/plain")
    if LOG_PATH.exists():
        with open(LOG_PATH, "rb") as f:
            return Response(f.read(), media_type="text/plain")
    return Response("Log file not found")
