from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager
from business.camera.exceptions import CameraNotFound


class GetCameraBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = None

    def set_params(self, camera_id: str):
        self._camera_id = camera_id
        return self

    def execute(self) -> Camera:
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        return camera