import logging
import asyncio

from module.conf import reload, VERSION
from .sub_thread import BemfaThread, DiandengThread

logger = logging.getLogger(__name__)

figlet = r"""
       _                   _                    _ 
 __  _(_) __ _  ___   __ _(_)    __      _____ | |
 \ \/ / |/ _` |/ _ \ / _` | |____\ \ /\ / / _ \| |
  >  <| | (_| | (_) | (_| | |_____\ V  V / (_) | |
 /_/\_\_|\__,_|\___/ \__,_|_|      \_/\_/ \___/|_|
"""


class Program(BemfaThread, DiandengThread):
    @staticmethod
    def __start_info():
        for line in figlet.splitlines():
            logger.info(line.strip("\n"))
        logger.info(f"Starting xiaoai-wol version:{VERSION}...")

    async def startup(self):
        self.__start_info()
        await self.start()

    async def start(self):
        self.stop_event.clear()
        reload()
        while not self.can_run:
            logger.warning("Platform subscribing thread is not running.")
            logger.info("Waiting for platform subscribing thread to start.")
            reload()
            await asyncio.sleep(30)
        if self.enable_bemfa:
            self.bemfa_start()
        if self.enable_diandeng:
            self.diandeng_start()
        logger.info("Platform subscribing thread running success.")
        return "第三方平台监听启动成功。"

    async def stop(self):
        logger.info("Platform subscribing thread stop.")
        if self.is_running:
            self.stop_event.set()
            self.bemfa_stop()
            self.diandeng_stop()
            return "第三方平台监听停止成功。"
        else:
            return "第三方平台监听未运行。"
