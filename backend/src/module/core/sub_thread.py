import threading
import time

from module.conf import config
from module.platform import PlatformClient
from .status import ProgramStatus


class BemfaThread(ProgramStatus):
    def __init__(self):
        super().__init__()
        self._clinet = PlatformClient()
        self._bemfa_thread = threading.Thread(
            target=self._clinet.__enter__,
        )

    def bemfa_start(self):
        self.bemfa_thread.start()

    def bemfa_stop(self):
        if self._bemfa_thread.is_alive():
            self._clinet.__exit__()
            self._bemfa_thread.join()

    @property
    def bemfa_thread(self):
        if not self._bemfa_thread.is_alive():
            self._bemfa_thread = threading.Thread(
                target=self._clinet.__enter__,
            )
        return self._bemfa_thread


class DiandengThread(ProgramStatus):
    def __init__(self):
        super().__init__()
        pass

    def diandeng_start(self):
        pass

    def diandeng_stop(self):
        pass
