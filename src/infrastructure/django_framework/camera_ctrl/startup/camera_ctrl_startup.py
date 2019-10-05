import logging

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException
from camera_ctrl.settings_facade import SettingsFacade


class CameraCtrlStartup:
    def __init__(self, camera_ctrl_service: CameraCtrlService):
        self._camera_ctrl_service = camera_ctrl_service

    def run(self):
        self._check_autodetect_cameras_action()

    def _check_autodetect_cameras_action(self):
        settings = SettingsFacade()
        if settings.autodetect_cameras_on_start:
            try:
                self._camera_ctrl_service.cameras_autodetect()

            except CameraException as e:
                logging.error('Failed to autodetect cameras on start. Error: {}'.format(e))