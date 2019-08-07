from django.db import models
from datetime import datetime, timedelta

from django.db.models.signals import post_delete
from django.dispatch import receiver
from django_apscheduler.models import DjangoJob


class Profile(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

    @staticmethod
    def build_default_profile():
        profile = Profile(name='default')
        profile.name = 'default'
        profile.save()

        shutterspeed = FavField()
        shutterspeed.profile = profile
        shutterspeed.name = 'shutterspeed'
        shutterspeed.save()

        iso = FavField()
        iso.profile = profile
        iso.name = 'iso'
        iso.save()

        return profile


class FavField(models.Model):
    profile = models.ForeignKey(Profile, related_name='fields', on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    def __str__(self):
        return '{0}/{1}'.format(self.profile.name, self.name)


class CronTimelapse(models.Model):
    name = models.CharField(max_length=64, default='My timelapse')
    storage_dir_format = models.CharField(max_length=256, default='~/Pictures/')
    filename_format = models.CharField(max_length=256, default='capture')

    start_date = models.DateTimeField(default=datetime.now, blank=True)
    end_date = models.DateTimeField(default=datetime.now() + timedelta(days=1), blank=True)

    year = models.CharField(max_length=128, default='*')
    month = models.CharField(max_length=128, default='*')
    day = models.CharField(max_length=256, default='*')
    week = models.CharField(max_length=256, default='*')
    day_of_week = models.CharField(max_length=256, default='*')
    hour = models.CharField(max_length=128, default='*')
    minute = models.CharField(max_length=128, default='*')
    second = models.CharField(max_length=128, default='*')

    capture_index = models.IntegerField(default=0)

    def __str__(self):
        return self.name


@receiver(post_delete, sender=CronTimelapse)
def auto_delete_publish_info_with_book(sender, instance: CronTimelapse, **kwargs):
    DjangoJob.objects.filter(name=str(instance.pk)).delete()