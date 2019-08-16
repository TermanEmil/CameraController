from business.scheduling.scheduler import Scheduler


class SchedulingStartupBlRule:
    def __init__(self, scheduler: Scheduler):
        self._scheduler = scheduler

    def execute(self):
        self._scheduler.start()