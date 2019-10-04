from django.db import models


class HistoryUnit(models.Model):
    log_type = models.CharField(max_length=32)
    category = models.CharField(max_length=32, null=True)
    title = models.CharField(max_length=64)
    content = models.CharField(max_length=256)

    created_time = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return '{}| {} - {}'.format(self.log_type, self.category, self.title)