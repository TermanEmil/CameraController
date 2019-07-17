from .camera import Camera


class CameraManager:
    def detect_all_cameras(self):
        raise NotImplementedError()

    @property
    def cameras(self) -> iter:
        raise NotImplementedError()

    def get_camera(self, camera_id) -> Camera:
        raise NotImplementedError()

    def remove_camera(self, camera_id):
        raise NotImplementedError()
