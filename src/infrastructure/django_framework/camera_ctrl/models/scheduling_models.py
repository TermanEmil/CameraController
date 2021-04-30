from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.urls import reverse
from django_apscheduler.models import DjangoJob


class CronSchedule(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    start_date = models.DateTimeField(blank=True)
    end_date = models.DateTimeField(blank=True)

    year = models.CharField(max_length=128, help_text='4 digit year')
    month = models.CharField(max_length=128, help_text='1-12')
    day = models.CharField(max_length=256, help_text='1-31')
    week = models.CharField(max_length=256, help_text='1-53')
    day_of_week = models.CharField(max_length=256, help_text='0-6 or mon, tue, wed, thu, fri, sat, sun')
    hour = models.CharField(max_length=128, help_text='0-23')
    minute = models.CharField(max_length=128, help_text='0-59')
    second = models.CharField(max_length=128, help_text='0-59')

    def clean(self):
        pass

    def __str__(self):
        return '{}_{}'.format(self.name, self.pk)

    def get_absolute_url(self):
        return reverse('cron/update', kwargs={'pk': self.pk})


class Timelapse(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(CronSchedule, on_delete=models.SET_NULL, null=True, blank=True)
    schedule_job_id = models.CharField(max_length=124, null=True)

    name = models.CharField(max_length=64, default='Timelapse')
    storage_dir_format = models.CharField(max_length=256, default='./Timelapses/{timelapse_name}_{timelapse_id}')
    filename_format = models.CharField(max_length=256, default='capture_{camera_id}_{capture_index}')
    capture_index = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('timelapse/update', kwargs={'pk': self.pk})


class ScheduledConfig(models.Model):
    id = models.AutoField(primary_key=True)
    schedule = models.ForeignKey(CronSchedule, on_delete=models.SET_NULL, null=True, blank=True)
    schedule_job_id = models.CharField(max_length=124, null=True)

    name = models.CharField(max_length=64, default='Scheduled Config')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('scheduled-config/list')


class ScheduledConfigField(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=124, null=False, blank=False)
    value = models.CharField(max_length=124)
    scheduled_config = models.ForeignKey(ScheduledConfig, on_delete=models.CASCADE, related_name='fields')


@receiver(post_delete, sender=Timelapse)
def auto_delete_timelapse_job(sender, instance: Timelapse, **kwargs):
    if instance.schedule_job_id:
        DjangoJob.objects.filter(id=instance.schedule_job_id).delete()


@receiver(post_delete, sender=ScheduledConfig)
def auto_delete_scheduled_config_job(sender, instance: ScheduledConfig, **kwargs):
    if instance.schedule_job_id:
        DjangoJob.objects.filter(id=instance.schedule_job_id).delete()
