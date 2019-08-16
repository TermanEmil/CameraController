from typing import Iterable, Callable

from business.scheduling.cron_schedule_repository import CronScheduleRepository
from business.scheduling.scheduler import Scheduler
from enterprise.scheduling.cron_schedule import CronSchedule


class CreateCronScheduleBlRule:
    def __init__(self, cron_schedule_repository: CronScheduleRepository):
        self._cron_schedule_repository = cron_schedule_repository
        self._cron_schedule = None

    def set_params(self, cron_schedule: CronSchedule):
        self._cron_schedule = cron_schedule
        return self

    def execute(self):
        self._cron_schedule_repository.add(model=self._cron_schedule)


class GetAllCronSchedulesBlRule:
    def __init__(self, cron_schedule_repository: CronScheduleRepository):
        self._cron_schedule_repository = cron_schedule_repository

    def execute(self) -> Iterable[CronSchedule]:
        return self._cron_schedule_repository.get_all()


class GetCronScheduleBlRule:
    def __init__(self, cron_schedule_repository: CronScheduleRepository):
        self._cron_schedule_repository = cron_schedule_repository
        self._pk = None

    def set_params(self, pk: int):
        self._pk = pk
        return self

    def execute(self) -> CronSchedule:
        return self._cron_schedule_repository.get(pk=self._pk)


class UpdateCronScheduleBlRule:
    def __init__(self, cron_schedule_repository: CronScheduleRepository):
        self._cron_schedule_repository = cron_schedule_repository
        self._schedule = None

    def set_params(self, schedule: CronSchedule):
        self._schedule = schedule
        return self

    def execute(self):
        self._cron_schedule_repository.update(model=self._schedule)


class DeleteCronScheduleBlRule:
    def __init__(self, cron_schedule_repository: CronScheduleRepository):
        self._cron_schedule_repository = cron_schedule_repository
        self._pk = None

    def set_params(self, pk: int):
        self._pk = pk
        return self

    def execute(self):
        self._cron_schedule_repository.remove(pk=self._pk)


class RunScheduleBlRule:
    def __init__(self, scheduler: Scheduler):
        self._scheduler = scheduler

    def execute(self, schedule: CronSchedule, func: Callable, func_kwargs: dict) -> str:
        return self._scheduler.add_job(func=func, func_kwargs=func_kwargs, cron_schedule=schedule)
