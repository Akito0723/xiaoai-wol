import asyncio
import logging

from fastapi import APIRouter

from module.conf import VERSION
from module.core import Program
from .response import APIResponse, gen_response

logger = logging.getLogger(__name__)
program = Program()
router = APIRouter(prefix="/program", tags=["program"])
is_running = None

@router.get(
    "/reStart", response_model=APIResponse
)
async def reStart():
    try:
        stop_msg = await program.stop()
        start_msg = await program.start()
        return gen_response(APIResponse(msg=start_msg, content=start_msg))
    except Exception as e:
        logger.error("Failed to start subscribing", exc_info=True)
        return gen_response(APIResponse(msg="操作失败。", code="9999", content=str(e)), httpCode=500)

@router.get(
    "/stop", response_model=APIResponse
)
async def stop():
    try:
        msg = await program.stop()
        return gen_response(APIResponse(msg=msg, content=msg))
    except Exception as e:
        logger.error("Failed to stop subscribing", exc_info=True)
        return gen_response(APIResponse(msg="操作失败。", code="9999", content=str(e)), httpCode=500)

@router.get("/status", response_model=APIResponse)
async def program_status(immediately: bool = False):
    global is_running
    if is_running is None:
        is_running = program.is_running
        return gen_response(APIResponse(content={
            "version": VERSION,
            "is_running": is_running,
            "can_run": program.can_run,
        }))
    if immediately:
        return gen_response(APIResponse(content={
            "version": VERSION,
            "is_running": program.is_running,
            "can_run": program.can_run,
        }))
    try:
        _is_running = program.is_running
        # 等待最大 30 秒，如果没有状态变化则超时
        timeout = 30
        start_time = asyncio.get_event_loop().time()

        while _is_running == is_running:
            # 每秒检查一次状态
            await asyncio.sleep(1)
            if asyncio.get_event_loop().time() - start_time > timeout:
                raise asyncio.TimeoutError("超时")
            _is_running = program.is_running

        # 状态发生变化后更新全局变量
        is_running = _is_running
        return gen_response(APIResponse(content={
            "version": VERSION,
            "is_running": _is_running,
            "can_run": program.can_run,
        }))

    except asyncio.TimeoutError:
        return gen_response(APIResponse(content={
            "version": VERSION,
            "is_running": program.is_running,
            "can_run": program.can_run,
        }))
