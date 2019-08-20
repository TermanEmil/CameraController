import logging

from django.core.mail import send_mail

from enterprise.camera_ctrl.camera import Camera
from proj_logging.internal_api.log_to_db import log_to_db, LogType
from proj_settings.settings_facade import SettingsFacade


def _get_log_msg(camera: Camera, error: str) -> str:
    return 'Camera {}: Failed to take picture. Error: {}'.format(camera.name, error)


def capture_error_log(camera: Camera, error: str, **kwargs):
    logging.error(_get_log_msg(camera, error))


def capture_error_send_email(camera: Camera, error: str, **kwargs):
    settings = SettingsFacade()
    if not settings.send_email_on_error:
        return

    try:
        send_mail(
            subject='Timelapse capture failed',
            message='Camera {} failed to capture an image. Error = {}'.format(camera.name, error),
            from_email='devemail42@gmail.com',
            recipient_list=list(settings.emails),
            fail_silently=False)

    except Exception as e:
        logging.error('Failed to send emails. Error: {}'.format(e))


def capture_error_log_to_db(camera: Camera, error: str, **kwargs):
    log_type = LogType.ERROR
    category = 'Timelapse'
    title = 'Failed capture'
    content = _get_log_msg(camera, error)

    log_to_db(log_type=log_type, category=category, title=title, content=content)