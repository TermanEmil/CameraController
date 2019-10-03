from django.urls import path

from camera_ctrl.views.camera_config.all_configs import AllConfigs
from camera_ctrl.views.camera_config.config_list import ConfigList
from camera_ctrl.views.camera_config.single_config import SingleConfig

urlpatterns = [
    path('all_configs/<str:camera_id>', AllConfigs.as_view(), name='all_configs'),
    path('config_list/<str:camera_id>', ConfigList.as_view(), name='config_list'),
    path('single_config/<str:camera_id>/<str:config_name>', SingleConfig.as_view(), name='single_config'),
]
