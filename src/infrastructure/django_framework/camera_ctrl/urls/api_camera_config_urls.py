from django.urls import path

from camera_ctrl.api.camera_config.camera_get_config import CameraGetConfigView
from camera_ctrl.api.camera_config.camera_set_config import CameraSetConfigView

urlpatterns = [
    path('api/cameras/<str:camera_id>/configs/<str:config_name>', CameraGetConfigView.as_view(), name='api_get_config'),
    path('api/cameras/<str:camera_id>/configs/<str:config_name>', CameraSetConfigView.as_view(), name='api_set_config'),
]
