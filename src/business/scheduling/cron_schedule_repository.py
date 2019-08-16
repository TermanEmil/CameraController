from typing import Iterable

from enterprise.scheduling.cron_schedule import CronSchedule


class CronScheduleRepository:
    def get_all(self) -> Iterable[CronSchedule]:
        raise NotImplementedError()

    def get(self, pk: int) -> CronSchedule:
        raise NotImplementedError()

    def add(self, model: CronSchedule):
        raise NotImplementedError()

    def update(self, model: CronSchedule):
        raise NotImplementedError()

    def remove(self, pk: int):
        raise NotImplementedError()