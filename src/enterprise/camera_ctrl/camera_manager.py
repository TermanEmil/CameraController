from threading import Lock

from enterprise.camera_ctrl.utils.multi_lock import MultiLock
from .camera import Camera
from typing import Iterable


class CameraManager:
    @property
    def sync_lock(self) -> Lock:
        raise NotImplementedError()

    @property
    def all_locks(self) -> MultiLock:
        # All locks that work with the system.
        raise NotImplementedError()

    @property
    def cameras(self) -> Iterable[Camera]:
        raise NotImplementedError()

    def detect_all_cameras(self):
        raise NotImplementedError()

    def get_camera(self, camera_id) -> Camera:
        raise NotImplementedError()

    def remove_camera(self, camera_id):
        raise NotImplementedError()

    def disconnect_all(self):
        raise NotImplementedError()