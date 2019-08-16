import os
from time import time

from enterprise.camera_ctrl.camera_manager import CameraManager
from business.camera.exceptions import CameraNotFound


class CaptureImgAndDownloadBlRule:
    def __init__(self, camera_manager: CameraManager):
        self._camera_manager = camera_manager
        self._camera_id = None

    def set_params(self, *, camera_id):
        self._camera_id = camera_id
        return self

    def execute(self) -> str:
        camera = self._camera_manager.get_camera(camera_id=self._camera_id)
        if camera is None:
            raise CameraNotFound()

        storage_dir = '/tmp/'
        filename = 'img_{0}_{1}_{2}'.format(camera.name, self._camera_id, time())
        file_path = camera.capture_img(storage_dir=storage_dir, filename_prefix=filename)

        if not os.path.exists(file_path):
            raise Exception('Failed to locally save the image')

        return file_path
