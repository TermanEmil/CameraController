from django.urls import re_path as url
from django.urls import path
from django.views.generic import RedirectView

from camera_ctrl.views.scheduling.cron.cron_schedule_crud import *
from camera_ctrl.views.scheduling.scheduled_config.scheduled_config_crud import ScheduledConfigCreate, \
    ScheduledConfigList, ScheduledConfigUpdate, ScheduledConfigDelete
from camera_ctrl.views.scheduling.timelapse.timelapse_crud import *

urlpatterns = [
    path('', TimelapseList.as_view(), name='scheduling'),

    path('cron/create', CronScheduleCreate.as_view(), name='cron/create'),
    path('cron/list', CronScheduleList.as_view(), name='cron/list'),
    path('cron/update/<int:pk>', CronScheduleUpdate.as_view(), name='cron/update'),
    path('cron/delete/<int:pk>', CronScheduleDelete.as_view(), name='cron/delete'),

    path('timelapse', TimelapseList.as_view(), name='timelapse/list'),
    path('timelapse/create', TimelapseCreate.as_view(), name='timelapse/create'),
    path('timelapse/<int:pk>', TimelapseUpdate.as_view(), name='timelapse/update'),
    path('timelapse/delete/<int:pk>', TimelapseDelete.as_view(), name='timelapse/delete'),

    path('scheduled-config', ScheduledConfigList.as_view(), name='scheduled-config/list'),
    path('scheduled-config/create', ScheduledConfigCreate.as_view(), name='scheduled-config/create'),
    path('scheduled-config/<int:pk>', ScheduledConfigUpdate.as_view(), name='scheduled-config/update'),
    path('scheduled-config/delete/<int:pk>', ScheduledConfigDelete.as_view(), name='scheduled-config/delete'),

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
