from enterprise.camera_ctrl.camera_manager import CameraManager
from business.camera.exceptions import CameraNotFound


class ReconnectBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = None

    def set_params(self, *, camera_id):
        self._camera_id = camera_id
        return self

    def execute(self):
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        camera.disconnect()