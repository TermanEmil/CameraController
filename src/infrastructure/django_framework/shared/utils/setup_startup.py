import sys
from typing import Callable


def setup_startup(startup_f: Callable):
    if 'runserver' not in sys.argv:
        return

    startup_f()