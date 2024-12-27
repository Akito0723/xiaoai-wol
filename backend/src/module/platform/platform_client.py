import logging
from module.conf import config

logger = logging.getLogger(__name__)


class PlatformClient:
    def __init__(self):
        super().__init__()
        self.client = self.__getClient()
        self.started = False

    @staticmethod
    def __getClient():
        if config["platform"]["type"] == "bemfa":
            from .client.bemfa_client import BemfaClient
            return BemfaClient()
        else:
            logger.error(f"[PlatformClient] Unsupported platform type: {type}")
            raise Exception(f"Unsupported platform type: {type}")

    def __enter__(self):
        if not self.started:
            self.started = True
            self.client.start()
        else:
            logger.error("[PlatformClient] Already started.")
        return self

    def __exit__(self):
        if self.started:
            self.client.stop()
            self.started = False



