from django.urls import path

from .factories import *


urlpatterns = [
    path('all_configs/<str:camera_id>', all_configs_view_factory(), name='all_configs'),
    path('config_list/<str:camera_id>', config_list_view_factory(), name='config_list'),
    path('single_config/<str:camera_id>/<str:config_name>', single_config_view_factory(), name='single_config'),
]
