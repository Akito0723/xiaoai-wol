import asyncio
import threading

from module.utils import Util
from module.conf import config

class ProgramStatus:
    def __init__(self):
        super().__init__()
        self._can_run = False
        self.stop_event = threading.Event()
        self.lock = threading.Lock()
        self.event = asyncio.Event()

    @property
    def is_running(self):
        if self.stop_event.is_set() or not Util.can_run():
            return False
        else:
            return True

    @property
    def is_stopped(self):
        return self.stop_event.is_set()

    @property
    def can_run(self):
        self._can_run = Util.can_run()
        return self._can_run

    @property
    def enable_bemfa(self):
        return config["platform"]["type"] == "bemfa"

    @property
    def enable_diandeng(self):
        return config["platform"]["type"] == "diandeng"
