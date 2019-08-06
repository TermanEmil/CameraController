from django.contrib import admin
from camera_control.models import Profile, FavField, CronTimelapse


# Register your models here.
admin.site.register(Profile)
admin.site.register(FavField)
admin.site.register(CronTimelapse)