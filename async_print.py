from threading import Lock

_g_print_lock = Lock()


def async_print(text):
    _g_print_lock.acquire()
    print(text)
    _g_print_lock.release()