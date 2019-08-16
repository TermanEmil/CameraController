from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager
from typing import Iterable


class GetAllCamerasBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager

    def execute(self) -> Iterable[Camera]:
        return self._camera_manager.cameras