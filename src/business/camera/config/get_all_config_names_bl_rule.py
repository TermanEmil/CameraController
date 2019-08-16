from typing import Iterable

from enterprise.camera_ctrl.camera_manager import CameraManager
from ..exceptions import CameraNotFound


class GetAllConfigNamesBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = None

    def set_params(self, camera_id: str):
        self._camera_id = camera_id
        return self

    def execute(self) -> Iterable[str]:
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        return camera.list_configs()
