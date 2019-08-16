from typing import Iterable

from business.scheduling import cron_schedule_repository
from enterprise.scheduling.cron_schedule import CronSchedule
from scheduling import models


class CronScheduleRepository(cron_schedule_repository.CronScheduleRepository):
    def get_all(self) -> Iterable[CronSchedule]:
        instances = models.CronSchedule.objects.all()

        for instance in instances:
            assert isinstance(instance, models.CronSchedule)

            schedule = CronSchedule(**vars(instance))
            schedule.pk = instance.pk
            yield schedule

    def get(self, pk: int) -> CronSchedule:
        instance = models.CronSchedule.objects.get(pk=pk)
        result = CronSchedule(**vars(instance))
        result.pk = instance.pk
        return result

    def add(self, model: CronSchedule):
        new_instance = models.CronSchedule.objects.create(**vars(model))
        new_instance.save()

    def update(self, model: CronSchedule):
        db_model = models.CronSchedule.objects.get(pk=model.pk)

        assert isinstance(db_model, models.CronSchedule)
        for atr, value in model.__dict__.items():
            setattr(db_model, atr, value)

        db_model.save()

    def remove(self, pk: int):
        db_model = models.CronSchedule.objects.get(pk=pk)
        assert isinstance(db_model, models.CronSchedule)
        db_model.delete()

