from enterprise.camera_ctrl.camera_manager import CameraManager
from ..exceptions import CameraNotFound, ConfigNotFound


class SetConfigBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = None
        self._config_name = None
        self._config_value = None

    def set_params(self, camera_id: str, config_name: str, config_value: str):
        self._camera_id = camera_id
        self._config_name = config_name
        self._config_value = config_value
        return self

    def execute(self):
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        field_config = camera.get_single_config(config_name=self._config_name)
        if field_config is None:
            raise ConfigNotFound()

        field_config.set_value(value=self._config_value)
        camera.set_config((field_config,))
