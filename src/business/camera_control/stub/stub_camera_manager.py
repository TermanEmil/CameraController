from ..camera_manager import CameraManager
from ..camera import Camera


class StubCameraManager(CameraManager):
    def __init__(self, cameras):
        self._cameras = {}
        self._cameras_to_detect = cameras

    @property
    def cameras(self):
        return self._cameras.values()

    def detect_all_cameras(self):
        for camera in self._cameras_to_detect:
            assert isinstance(camera, Camera)
            self._cameras[camera.id] = camera

    def get_camera(self, camera_id):
        return self._cameras.get(camera_id)
