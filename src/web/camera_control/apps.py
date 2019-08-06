from django.apps import AppConfig


class CameraControlConfig(AppConfig):
    name = 'camera_control'

    def ready(self):
        try:
            init_scheduler()
        except Exception as e:
            print('Failed to initialized apscheduler')


def init_scheduler():
    from factories import ApSchedulerFactory
    from django_apscheduler.jobstores import DjangoJobStore, register_events
    from django_apscheduler.models import DjangoJobExecution

    scheduler = ApSchedulerFactory.get()
    scheduler.add_jobstore(DjangoJobStore(), 'default')
    register_events(scheduler)

    # Delete job executions older than 7 days
    DjangoJobExecution.objects.delete_old_job_executions(604_800)

    scheduler.start()
