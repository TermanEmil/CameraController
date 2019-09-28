from adapters.camera.configs.camera_config_service import CameraConfigService
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from camera_ctrl.api.cameras_hard_reset_all import CamerasHardResetAll
from camera_ctrl.startup import CameraCtrlStartup
from shared.di import obj_graph
from .api.camera_capture_img_and_download import CameraCaptureImgAndDownload
from .api.camera_preview_source import CameraPreviewSource
from .api.camera_reconnect import CameraReconnect
from .api.camera_remove import CameraRemove
from .api.cameras_autodetect import CamerasAutodetect
from .views.index import Index
from .views.multi_preview import MultiPreview
from .views.single_preview import SinglePreview


def startup_factory() -> CameraCtrlStartup:
    return obj_graph().provide(CameraCtrlStartup)


def index_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return Index.as_view(camera_ctrl_service=camera_ctrl_service)


def single_preview_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    camera_config_service = obj_graph().provide(CameraConfigService)

    return SinglePreview.as_view(
        camera_ctrl_service=camera_ctrl_service,
        camera_config_service=camera_config_service)


def multi_preview_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return MultiPreview.as_view(camera_ctrl_service=camera_ctrl_service)


def cameras_autodetect_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CamerasAutodetect.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_remove_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CameraRemove.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_reconnect_view_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CameraReconnect.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_capture_img_and_download_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CameraCaptureImgAndDownload.as_view(
        camera_ctrl_service=camera_ctrl_service)


def camera_preview_source_factory():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CameraPreviewSource.as_view(camera_ctrl_service=camera_ctrl_service)


def cameras_hard_reset_all():
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    return CamerasHardResetAll.as_view(camera_ctrl_service=camera_ctrl_service)