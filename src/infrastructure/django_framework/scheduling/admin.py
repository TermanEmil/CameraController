from django.contrib import admin

# Register your models here.
from scheduling.models import CronSchedule, Timelapse


class CronScheduleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'start_date', 'end_date']


admin.site.register(CronSchedule, CronScheduleAdmin)
admin.site.register(Timelapse)