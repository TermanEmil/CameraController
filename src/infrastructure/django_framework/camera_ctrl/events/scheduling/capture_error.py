import logging

from adapters.emailing.email_service import EmailService
from camera_ctrl.log_to_db import LogType, log_to_db
from enterprise.camera_ctrl.camera import Camera
from proj_settings.settings_facade import SettingsFacade


def get_log_msg(camera: Camera, error: str) -> str:
    return '{}: Failed to take picture. Error: {}'.format(camera.name, error)


def capture_error_log(camera: Camera, error: str, **kwargs):
    logging.error(get_log_msg(camera, error))


def capture_error_log_to_db(camera: Camera, error: str, **kwargs):
    log_type = LogType.ERROR
    category = 'Timelapse'
    title = 'Failed capture'
    content = get_log_msg(camera, error)

    log_to_db(log_type=log_type, category=category, title=title, content=content)


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
