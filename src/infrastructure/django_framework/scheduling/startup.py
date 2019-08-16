from adapters.scheduling.schedule_service import ScheduleService
import logging


class Startup:
    def __init__(self, schedule_service: ScheduleService):
        self._schedule_service = schedule_service

    def run(self):
        try:
            self._schedule_service.run_startup_logic()

        except Exception as e:
            logging.critical('Failed to run schedule_id startup. Error = {}'.format(e))