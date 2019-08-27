from threading import Lock
from typing import List


class MultiLock:
    def __init__(self, locks: List[Lock]):
        self._locks = locks

    def __enter__(self):
        for l in self._locks:
            l.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        for l in self._locks:
            l.release()