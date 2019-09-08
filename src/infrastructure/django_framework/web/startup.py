import logging

from business.messaging.event_manager import EventManager


class WebStartup:
    def __init__(self, event_manager: EventManager):
        self._event_manager = event_manager

    def run(self):
        logging.getLogger('apscheduler').setLevel(logging.ERROR)
        self._event_manager.clear()