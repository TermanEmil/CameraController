from django.contrib import admin

# Register your models here.
from camera_ctrl.models import CronSchedule, Timelapse, HistoryUnit
from camera_ctrl.models.app_settings_models import GeneralSettings
from camera_ctrl.models.camera_config_models import FavField


class CronScheduleAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'start_date', 'end_date']


admin.site.register(FavField)
admin.site.register(CronSchedule, CronScheduleAdmin)
admin.site.register(Timelapse)
admin.site.register(HistoryUnit)
admin.site.register(GeneralSettings)