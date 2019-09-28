from business.camera.exceptions import CameraNotFoundException
from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager


class GetCameraBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager

    def execute(self, camera_id) -> Camera:
        camera = self._camera_manager.get_camera(camera_id=camera_id)
        if camera is None:
            raise CameraNotFoundException()

        return camera