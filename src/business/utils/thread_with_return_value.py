from threading import Thread
import queue


class ThreadWithReturnValue:
    def __init__(self, target, args):
        self._queue = queue.Queue()
        self._thread = Thread(target=lambda q, args_: q.put(target(*args_)), args=(self._queue, args))

    def start(self):
        self._thread.start()

    def join(self):
        self._thread.join()
        return self._queue.get()
