from typing import Callable

from enterprise.scheduling.cron_schedule import CronSchedule


class Scheduler:
    def start(self):
        raise NotImplementedError()

    def add_job(self, func: Callable, func_kwargs: dict, cron_schedule: CronSchedule):
        raise NotImplementedError()

    def modify(self, cron_schedule: CronSchedule):
        raise NotImplementedError()

    def delete(self, cron_schedule_id: int):
        raise NotImplementedError()

    def delete_job(self, job_id):
        raise NotImplementedError()