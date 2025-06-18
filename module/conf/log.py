import logging
import sys
import os
import io
from pathlib import Path

from .config_loader import config, VERSION

LOG_ROOT = Path("data/log")
LOG_PATH = LOG_ROOT / "log.txt"
STRING_IO = io.StringIO()


def setup_logger(level: int = logging.INFO):
    handlers = []
    if config["log"]["debug_enable"]:
        level = logging.DEBUG

    if VERSION == "DEV_VERSION":
        level = logging.DEBUG
        stream_handler = logging.StreamHandler(STRING_IO)
        handlers.append(stream_handler)
        handlers.append(logging.StreamHandler(sys.stdout))
    else:
        os.makedirs(os.path.dirname(LOG_PATH.resolve()), exist_ok=True)
        handlers.append(logging.FileHandler(LOG_PATH, encoding="utf-8"))
        handlers.append(logging.StreamHandler())

    logging.addLevelName(logging.DEBUG, "DEBUG:")
    logging.addLevelName(logging.INFO, "INFO:")
    logging.addLevelName(logging.WARNING, "WARNING:")
    LOGGING_FORMAT = "[%(asctime)s] %(levelname)-8s  %(message)s"
    TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
    logging.basicConfig(
        level=level,
        format=LOGGING_FORMAT,
        datefmt=TIME_FORMAT,
        encoding="utf-8",
        handlers=handlers,
    )
