from enterprise.camera_ctrl.camera_manager import CameraManager


class AutodetectBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager

    def execute(self):
        self._camera_manager.detect_all_cameras()