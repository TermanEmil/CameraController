from django.urls import path

from camera_ctrl.api.camera_config.camera_configs import CameraConfigsView

urlpatterns = [
    path('api/cameras/<str:camera_id>/configs/<str:config_name>', CameraConfigsView.as_view(), name='api_config'),
]
