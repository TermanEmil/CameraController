from enterprise.camera_ctrl.camera_config import CameraConfigField
from enterprise.camera_ctrl.camera_manager import CameraManager
from ..exceptions import CameraNotFound, ConfigNotFound


class GetConfigBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = ''
        self._config_name = ''

    def set_params(self, camera_id: str, config_name: str):
        self._camera_id = camera_id
        self._config_name = config_name
        return self

    def execute(self) -> CameraConfigField:
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        config = camera.get_single_config(config_name=self._config_name)
        if config is None:
            raise ConfigNotFound()

        return config
