from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from scheduling.views.cron.cron_schedule_crud import CronScheduleCreate, CronScheduleList
from scheduling.views.timelapse.timelapse_crud import TimelapseList, TimelapseDelete
from shared.utils.setup_startup import setup_startup
from .factories import *


setup_startup(lambda: startup_factory().run())

urlpatterns = [
    path('', TimelapseList.as_view(), name='scheduling'),

    path('cron/create', CronScheduleCreate.as_view(), name='cron/create'),
    path('cron/list', CronScheduleList.as_view(), name='cron/list'),
    path('cron/update/<int:pk>', cron_schedule_update_view_factory(), name='cron/update'),
    path('cron/delete/<int:pk>', cron_schedule_delete_view_factory(), name='cron/delete'),

    path('timelapse', TimelapseList.as_view(), name='timelapse/list'),
    path('timelapse/create', timelapse_create_view_factory(), name='timelapse/create'),
    path('timelapse/<int:pk>', timelapse_update_view_factory(), name='timelapse/update'),
    path('timelapse/delete/<int:pk>', TimelapseDelete.as_view(), name='timelapse/delete'),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
