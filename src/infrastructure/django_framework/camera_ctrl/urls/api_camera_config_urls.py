from django.urls import path

from camera_ctrl.api.camera_config.camera_set_config import CameraSetConfigView

urlpatterns = [
    path('api/cameras/<str:camera_id>/configs', CameraSetConfigView.as_view(), name='api_set_config'),
]
