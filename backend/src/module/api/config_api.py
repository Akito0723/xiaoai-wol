import logging

from fastapi import APIRouter
from pydantic import BaseModel
from .response import APIResponse, gen_response
from module.conf import config
from module.conf import save as save_config
from typing import Dict

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/config", tags=["config"])

class ScanNetworkRequest(BaseModel):
    network: str

@router.get(
    "/getConfig", response_model=APIResponse
)
def getConfig():
    try:
        return gen_response(APIResponse(content=config))
    except Exception as e:
        logger.error("Failed to get config", exc_info=True)
        return gen_response(APIResponse(msg="操作失败。", code="9999", content=str(e)))

@router.post(
    "/saveConfig", response_model=APIResponse
)
def saveConfig(request: Dict[str, object]):
    try:
        save_config(request)
        return gen_response(APIResponse())
    except Exception as e:
        logger.error("Failed to get config", exc_info=True)
        return gen_response(APIResponse(msg="操作失败。", code="9999", content=str(e)))

