from adapters.camera.configs.camera_config_service import CameraConfigService
from camera_config.views.config_list import ConfigList
from camera_config.views.single_config import SingleConfig
from .views.all_configs import AllConfigs
from shared.di import obj_graph


def all_configs_view_factory():
    camera_config_service = obj_graph().provide(CameraConfigService)
    return AllConfigs.as_view(camera_config_service=camera_config_service)


def config_list_view_factory():
    camera_config_service = obj_graph().provide(CameraConfigService)
    return ConfigList.as_view(camera_config_service=camera_config_service)


def single_config_view_factory():
    camera_config_service = obj_graph().provide(CameraConfigService)
    return SingleConfig.as_view(camera_config_service=camera_config_service)
