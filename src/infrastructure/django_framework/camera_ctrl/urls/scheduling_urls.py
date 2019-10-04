from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

from camera_ctrl.views.scheduling.cron.cron_schedule_crud import *
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

    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
]
