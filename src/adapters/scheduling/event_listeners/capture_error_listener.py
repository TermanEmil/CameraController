import logging

from adapters.app_logging.persistent_logger import PersistentLogger
from adapters.emailing.email_service import EmailService
from adapters.scheduling.notifications_settings import NotificationsSettings
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogType
from enterprise.camera_ctrl.camera import Camera
from ._format_capture_error_msg import format_capture_error_msg


class CaptureErrorListener(PersistentLogger):
    log_type = LogType.ERROR
    category = 'Timelapse'
    title = 'Capture failed'

    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            log_manager: LogManager,
            email_service: EmailService):

        super().__init__(log_manager)
        self._settings = notifications_settings
        self._log_manager = log_manager
        self._email_service = email_service

    def run(self, camera: Camera, error: str, **kwargs):
        msg = format_capture_error_msg(camera=camera, error=error)

        logging.error(msg)

        if self._settings.persistent_log_on_capture_error:
            self.persistent_log(msg)

        if self._settings.email_log_on_capture_error:
            self._email_log(msg)

    def _email_log(self, msg):
        self._email_service.send_email(subject=self.title, message=msg)

