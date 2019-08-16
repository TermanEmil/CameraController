from business.timelapse.get_timelapse_func_bl_rule import GetTimelapseFuncBlRule
from business.scheduling.cron_bl_rules import RunScheduleBlRule
from business.scheduling.scheduler import Scheduler
from business.scheduling.scheduling_startup_bl_rule import SchedulingStartupBlRule
from business.scheduling.timelapse_repository import TimelapseRepository
from enterprise.scheduling.cron_schedule import CronSchedule


class ScheduleService:
    def __init__(
            self,
            timelapse_repository: TimelapseRepository,
            scheduling_startup_bl_rule: SchedulingStartupBlRule,
            run_schedule_bl_rule: RunScheduleBlRule,
            get_timelapse_func_bl_rule: GetTimelapseFuncBlRule,
            scheduler: Scheduler):

        self._timelapse_repository = timelapse_repository
        self._scheduling_startup_bl_rule = scheduling_startup_bl_rule
        self._run_schedule_bl_rule = run_schedule_bl_rule
        self._get_timelapse_func_bl_rule = get_timelapse_func_bl_rule

        self._scheduler = scheduler

    def run_startup_logic(self):
        self._scheduling_startup_bl_rule.execute()

    def run_timelapse(self, timelapse_pk: int, cron_schedule: CronSchedule) -> str:
        dto = self._get_timelapse_func_bl_rule.execute(timelapse_pk)
        return self._run_schedule_bl_rule.execute(schedule=cron_schedule, func=dto.func, func_kwargs=dto.kwargs)

    def delete_job(self, job_id):
        self._scheduler.delete_job(job_id)