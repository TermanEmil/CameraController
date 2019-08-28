from django.db import models


class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class GeneralSettings(SingletonModel):
    send_email_on_timelapse_error = models.BooleanField(default=True)
    hard_reset_on_timelapse_error = models.BooleanField(default=True)
    send_email_on_sync_error = models.BooleanField(default=True)
    seconds_to_wait_after_hard_reset = models.FloatField(default=5.0)

    send_email_on_capture_error = models.BooleanField(default=False)

    log_to_db_timelapse_capture = models.BooleanField(default=False, verbose_name='Log timelapse capture')
    log_to_db_camera_capture = models.BooleanField(default=True, verbose_name='Log camera capture')

    autodetect_cameras_on_start = models.BooleanField(default=True)

    emails = models.CharField(max_length=512, blank=True, help_text='Space separated emails')

    @staticmethod
    def get() -> 'GeneralSettings':
        GeneralSettings.load()
        return GeneralSettings.objects.get(pk=1)