from threading import Lock
from typing import Iterable

from .camera import Camera
from .multi_lock import MultiLock


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