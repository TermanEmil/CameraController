from threading import Lock
from typing import Dict

from enterprise.camera_ctrl.camera_manager import CameraManager
from enterprise.camera_ctrl.multi_lock import MultiLock
from infrastructure.camera_glue_code.stub.stub_camera import StubCamera


class StubCameraManager(CameraManager):
    def __init__(self, cameras):
        self._cameras: Dict[StubCamera] = dict()
        self._cameras_to_detect = cameras
        self._stub_lock = Lock()

    @property
    def all_locks(self) -> MultiLock:
        locks = [camera.sync_lock for camera in self.cameras]
        locks.append(self._stub_lock)
        return MultiLock(locks)

    @property
    def sync_lock(self) -> Lock:
        return self._stub_lock

    @property
    def cameras(self):
        return self._cameras.values()

    def detect_all_cameras(self):
        for camera in self._cameras_to_detect:
            self._cameras[camera.id] = camera

    def disconnect_all(self):
        self._cameras.clear()

    def get_camera(self, camera_id):
        return self._cameras.get(camera_id)

    def remove_camera(self, camera_id):
        if camera_id in self._cameras:
            self._cameras.pop(camera_id)
