import logging
from datetime import datetime

from adapters.scheduling.notifications_settings import NotificationsSettings
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType
from enterprise.camera_ctrl.camera import Camera


class CaptureTakenListener:
    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            log_manager: LogManager):

        self._settings = notifications_settings
        self._log_manager = log_manager

    def run(self, camera: Camera, filepath: str, **kwargs):
        msg = '{}: Photo taken to {}'.format(camera.name, filepath)

        logging.info(msg)

        if self._settings.persistent_log_on_capture_taken:
            self._persistent_log(msg)

    def _persistent_log(self, msg):
        log_message = LogMessage(
            log_type=LogType.INFO,
            category='Timelapse',
            title='Photo taken',
            content=msg,
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)