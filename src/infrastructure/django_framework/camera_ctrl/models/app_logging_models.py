from django.db import models

from enterprise.app_logging.log_message import LogMessage


class HistoryUnitManager(models.Manager):
    def create_from_log_message(self, log_message: LogMessage):
        self.create(
            log_type=log_message.log_type.value,
            category=log_message.category,
            title=log_message.title,
            content=log_message.content,
            created_time=log_message.created_time)


class HistoryUnit(models.Model):
    id = models.AutoField(primary_key=True)
    log_type = models.CharField(max_length=32)
    category = models.CharField(max_length=32, null=True)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)
    created_time = models.DateTimeField(auto_now=True, null=True)

    objects = HistoryUnitManager()

    def __str__(self):
        return '{}| {} - {}'.format(self.log_type, self.category, self.title)

