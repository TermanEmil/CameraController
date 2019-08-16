from .camera import Camera
from typing import Iterable


class CameraManager:
    def detect_all_cameras(self):
        raise NotImplementedError()

    @property
    def cameras(self) -> Iterable[Camera]:
        raise NotImplementedError()

    def get_camera(self, camera_id) -> Camera:
        raise NotImplementedError()

    def remove_camera(self, camera_id):
        raise NotImplementedError()
