from adapters.camera.configs.camera_config_service import CameraConfigService
from adapters.camera.configs.favourite_configs_service import FavouriteConfigsService
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from shared.di import obj_graph
from .api.camera_capture_img_and_download import CameraCaptureImgAndDownload
from .api.camera_preview_source import CameraPreviewSource
from .api.camera_reconnect import CameraReconnect
from .api.camera_remove import CameraRemove
from .api.cameras_autodetect import CamerasAutodetect
from .app_obj_mapper import AppObjectMapper
from .views.index import Index
from .views.multi_preview import MultiPreview
from .views.single_preview import SinglePreview


def index_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    obj_mapper = AppObjectMapper()
    return Index.as_view(camera_ctrl_service=camera_ctrl_service, obj_mapper=obj_mapper)


def single_preview_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    camera_config_service = obj_graph.provide(CameraConfigService)
    obj_mapper = AppObjectMapper()

    return SinglePreview.as_view(
        camera_ctrl_service=camera_ctrl_service,
        camera_config_service=camera_config_service,
        obj_mapper=obj_mapper)


def multi_preview_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    obj_mapper = AppObjectMapper()
    return MultiPreview.as_view(camera_ctrl_service=camera_ctrl_service, obj_mapper=obj_mapper)


def cameras_autodetect_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    return CamerasAutodetect.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_remove_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    return CameraRemove.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_reconnect_view_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    return CameraReconnect.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_capture_img_and_download_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    return CameraCaptureImgAndDownload.as_view(camera_ctrl_service=camera_ctrl_service)


def camera_preview_source_factory():
    camera_ctrl_service = obj_graph.provide(CameraCtrlService)
    return CameraPreviewSource.as_view(camera_ctrl_service=camera_ctrl_service)