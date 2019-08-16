import sys

from django.apps import AppConfig


class SchedulingConfig(AppConfig):
    name = 'scheduling'

    def ready(self):
        if 'runserver' not in sys.argv:
            return

        from .factories import startup_factory

        startup = startup_factory()
        startup.run()