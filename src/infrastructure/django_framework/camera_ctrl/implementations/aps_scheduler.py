from typing import Callable

from apscheduler.schedulers.base import BaseScheduler
from django_apscheduler.jobstores import DjangoJobStore

from business.scheduling.scheduler import Scheduler
from camera_ctrl.models import Timelapse
from enterprise.scheduling.cron_schedule import CronSchedule


class ApsScheduler(Scheduler):
    def __init__(self, aps_scheduler: BaseScheduler):
        self._scheduler = aps_scheduler

    def start(self):
        self._scheduler.add_jobstore(DjangoJobStore(), 'default')
        self._scheduler.start()

    def add_job(self, func: Callable, func_kwargs: dict, cron_schedule: CronSchedule) -> str:
        job = self._scheduler.add_job(
            func=func,
            kwargs=func_kwargs,
            trigger='cron',

            start_date=cron_schedule.start_date,
            end_date=cron_schedule.end_date,

            year=cron_schedule.year,
            month=cron_schedule.month,
            day=cron_schedule.day,
            week=cron_schedule.week,
            day_of_week=cron_schedule.day_of_week,

            second=cron_schedule.second,
            minute=cron_schedule.minute,
            hour=cron_schedule.hour)

        return job.id

    def modify(self, cron_schedule: CronSchedule):
        for job_id in self._get_all_affected_job_ids(cron_schedule.pk):
            self._scheduler.reschedule_job(
                job_id,
                trigger='cron',

                start_date=cron_schedule.start_date,
                end_date=cron_schedule.end_date,

                year=cron_schedule.year,
                month=cron_schedule.month,
                day=cron_schedule.day,
                week=cron_schedule.week,
                day_of_week=cron_schedule.day_of_week,

                second=cron_schedule.second,
                minute=cron_schedule.minute,
                hour=cron_schedule.hour)

    def delete(self, cron_schedule_id: int):
        for job_id in self._get_all_affected_job_ids(cron_schedule_id):
            self._scheduler.remove_job(job_id)

    def delete_job(self, job_id):
        self._scheduler.remove_job(job_id)

    @staticmethod
    def _get_all_affected_job_ids(cron_schedule_id):
        objs = Timelapse.objects.filter(schedule_id=cron_schedule_id)
        for obj in objs:
            assert isinstance(obj, Timelapse)
            yield obj.schedule_job_id