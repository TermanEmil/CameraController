from datetime import datetime

from business.app_logging.log_manager import LogManager
from camera_ctrl.settings_facade import SettingsFacade
from enterprise.app_logging.log_message import LogMessage, LogType
from enterprise.camera_ctrl.camera import Camera
import logging


def _get_log_msg(camera: Camera, filepath: str):
    return '{}: Photo taken to {}'.format(camera.name, filepath)


def photo_taken_log(camera: Camera, filepath: str, **kwargs):
    logging.info(_get_log_msg(camera, filepath))


class PhotoTakenPersistentLog:
    def __init__(self, log_manager: LogManager, settings_facade: SettingsFacade):
        self._log_manager = log_manager
        self._settings = settings_facade

    def run(self, camera: Camera, filepath: str, **kwargs):
        if not self._settings.log_to_db_camera_capture:
            return

        log_message = LogMessage(
            log_type=LogType.INFO,
            category='Timelapse',
            title='Photo taken',
            content=_get_log_msg(camera, filepath),
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)