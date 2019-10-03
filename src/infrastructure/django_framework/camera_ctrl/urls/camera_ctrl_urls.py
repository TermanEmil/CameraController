from django.urls import path

from camera_ctrl.api.camera_ctrl.camera_capture_img_and_download import CameraCaptureImgAndDownload
from camera_ctrl.api.camera_ctrl.camera_preview_source import CameraPreviewSource
from camera_ctrl.api.camera_ctrl.camera_reconnect import CameraReconnect
from camera_ctrl.api.camera_ctrl.camera_remove import CameraRemove
from camera_ctrl.api.camera_ctrl.cameras_autodetect import CamerasAutodetect
from camera_ctrl.api.camera_ctrl.cameras_hard_reset_all import CamerasHardResetAll
from camera_ctrl.views.camera_ctrl.index import Index
from camera_ctrl.views.camera_ctrl.multi_preview import MultiPreview
from camera_ctrl.views.camera_ctrl.single_preview import SinglePreview

urlpatterns = (
    path('', Index.as_view(), name='index'),
    path('index', Index.as_view(), name='index'),
    path('single_preview/<str:camera_id>', SinglePreview.as_view(), name='single_preview'),
    path('multi_preview', MultiPreview.as_view(), name='multi_preview'),

    path('api/cameras_autodetect', CamerasAutodetect.as_view(), name='api/cameras_autodetect'),
    path('api/camera_remove/<str:camera_id>', CameraRemove.as_view()),
    path('api/camera_reconnect/<str:camera_id>', CameraReconnect.as_view()),
    path('api/camera_preview_source/<str:camera_id>', CameraPreviewSource.as_view(), name='api/camera_preview_source'),
    path('api/cameras_hard_reset_all', CamerasHardResetAll.as_view(), name='api/cameras_hard_reset_all'),
    path('api/camera_capture_img_and_download/<str:camera_id>', CameraCaptureImgAndDownload.as_view(), name='camera_capture_img_and_download'),
)