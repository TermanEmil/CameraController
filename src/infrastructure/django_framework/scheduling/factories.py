from adapters.scheduling.schedule_service import ScheduleService
from scheduling.implementations.aps_scheduler import ApsScheduler
from scheduling.startup import Startup
from scheduling.views.cron.cron_schedule_crud import CronScheduleUpdate, CronScheduleDelete
from scheduling.views.timelapse.timelapse_crud import TimelapseCreate, TimelapseUpdate
from shared.di import obj_graph


def startup_factory() -> Startup:
    return obj_graph().provide(Startup)


def timelapse_create_view_factory():
    schedule_service = obj_graph().provide(ScheduleService)
    return TimelapseCreate.as_view(schedule_service=schedule_service)


def timelapse_update_view_factory():
    schedule_service = obj_graph().provide(ScheduleService)
    return TimelapseUpdate.as_view(schedule_service=schedule_service)


def cron_schedule_update_view_factory():
    scheduler = obj_graph().provide(ApsScheduler)
    return CronScheduleUpdate.as_view(scheduler=scheduler)


def cron_schedule_delete_view_factory():
    scheduler = obj_graph().provide(ApsScheduler)
    return CronScheduleDelete.as_view(scheduler=scheduler)