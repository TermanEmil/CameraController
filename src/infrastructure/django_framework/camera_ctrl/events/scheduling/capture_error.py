import logging
from datetime import datetime

from adapters.emailing.email_service import EmailService
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType
from enterprise.camera_ctrl.camera import Camera
from proj_settings.settings_facade import SettingsFacade


def get_log_msg(camera: Camera, error: str) -> str:
    return '{}: Failed to take picture. Error: {}'.format(camera.name, error)


def capture_error_log(camera: Camera, error: str, **kwargs):
    logging.error(get_log_msg(camera, error))


class CaptureErrorPersistentLog:
    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def run(self, camera: Camera, error: str, **kwargs):
        log_message = LogMessage(
            log_type=LogType.ERROR,
            category='Timelapse',
            title='Failed capture',
            content=get_log_msg(camera, error),
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)


class CaptureErrorSendEmail:
    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    def run(self, camera: Camera, error: str, **kwargs):
        settings = SettingsFacade()
        if not settings.send_email_on_capture_error:
            return

        subject = 'Capture failed'
        message = get_log_msg(camera, error)

        try:
            self._email_service.send_email(subject=subject, message=message)

        except Exception as e:
            logging.error('Failed to send emails. Error: {}'.format(e))
