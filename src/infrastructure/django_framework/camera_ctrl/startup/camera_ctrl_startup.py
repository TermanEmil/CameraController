import logging

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException
from camera_ctrl.settings.camera_ctrl_settings import CameraCtrlSettings


class CameraCtrlStartup:
    def __init__(
            self,
            camera_ctrl_service: CameraCtrlService,
            camera_ctrl_settings: CameraCtrlSettings):

        self._camera_ctrl_service = camera_ctrl_service
        self._camera_ctrl_settings = camera_ctrl_settings

    def run(self):
        if self._camera_ctrl_settings.autodetect_cameras_on_start:
            self._autodetect_cameras()

    def _autodetect_cameras(self):
        try:
            self._camera_ctrl_service.cameras_autodetect()

        except CameraException as e:
            logging.error('Failed to autodetect cameras on start. Error: {}'.format(e))