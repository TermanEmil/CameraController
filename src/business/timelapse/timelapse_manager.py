from apscheduler.schedulers.base import BaseScheduler


class TimelapseManager:
    def __init__(self, scheduler: BaseScheduler):
        self._scheduler = scheduler

    def create_timelapse(self, timelapse_model):
        pass