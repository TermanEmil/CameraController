import os
from time import time

from business.camera.get_camera_bl_rule import GetCameraBlRule
from enterprise.camera_ctrl.camera_manager import CameraManager
from business.camera.exceptions import CameraNotFoundException


class CaptureImgAndDownloadBlRule:
    storage_dir = '/tmp/'

    def __init__(
            self,
            camera_manager: CameraManager,
            get_camera_bl_rule: GetCameraBlRule):

        self._camera_manager = camera_manager
        self._get_camera_bl_rule = get_camera_bl_rule

    def execute(self, camera_id) -> str:
        camera = self._get_camera_bl_rule.execute(camera_id=camera_id)

        filename = 'img_{0}_{1}_{2}'.format(camera.name, camera_id, time())
        file_path = camera.capture_img(
            storage_dir=self.storage_dir,
            filename_prefix=filename)

        if not os.path.exists(file_path):
            raise Exception('Failed to locally save the image')

        return file_path
