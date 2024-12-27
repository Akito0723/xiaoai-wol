import asyncio
import logging
import os

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from module.api import v1
from module.conf import VERSION, config, setup_logger
from module.core.program import Program

# 初始化日志
setup_logger()
logger = logging.getLogger(__name__)
uvicorn_logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": logger.handlers,
    "loggers": {
        "uvicorn": {
            "level": logger.level,
        },
        "uvicorn.access": {
            "level": "WARNING",
        },
    },
}
program = Program()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # 启动后台
    task = asyncio.create_task(program.startup())
    yield
    await program.stop()


def create_app() -> FastAPI:
    _app = FastAPI(lifespan=lifespan)
    _app.include_router(v1, prefix="/api")
    return _app


app = create_app()
# 配置静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/js", StaticFiles(directory="static/js"), name="js")
app.mount("/css", StaticFiles(directory="static/css"), name="css")
app.mount("/images", StaticFiles(directory="static/images"), name="images")


@app.get("/", response_class=HTMLResponse)
async def get_default_page():
    with open(os.path.join("static", "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)


if __name__ == "__main__":
    if os.getenv("IPV6"):
        host = "::"
    else:
        host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run(
        app,
        host=host,
        port=config["server"]["port"],
        log_config=uvicorn_logging_config,
    )
