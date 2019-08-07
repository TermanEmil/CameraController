from django.contrib import admin
from camera_control.models import Profile, FavField, CronTimelapse


class CronTimelapseAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'capture_index']


# Register your models here.
admin.site.register(Profile)
admin.site.register(FavField)
admin.site.register(CronTimelapse, CronTimelapseAdmin)