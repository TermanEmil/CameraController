import logging
from typing import Iterable

from django.core.mail import send_mail

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from adapters.emailing.email_service import EmailService
from enterprise.camera_ctrl.camera import Camera
from enterprise.scheduling.timelapse import Timelapse
from proj_settings.settings_facade import SettingsFacade
from . import capture_error


def _get_error_msgs(errors: Iterable[dict]):
    for error in errors:
        camera: Camera = error['camera']
        error_msg: str = error['error']

        yield capture_error.get_log_msg(camera=camera, error=error_msg)


def _get_log_msg(timelapse: Timelapse, errors: Iterable[dict]) -> str:
    msg = '--- {}: finished with errors. Capture index = {}'.format(timelapse.name, timelapse.capture_index)
    msg += '\n'
    msg += '\n'.join(_get_error_msgs(errors))
    return msg


class TimelapseErrorSendEmail:
    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    def run(self, timelapse: Timelapse, errors: Iterable[dict], **kwargs):
        settings = SettingsFacade()
        if not settings.send_email_on_timelapse_error:
            return

        subject = 'Timelapse failed'
        message = _get_log_msg(timelapse, errors)

        try:
            self._email_service.send_email(subject=subject, message=message)

        except Exception as e:
            logging.error('Failed to send emails. Error: {}'.format(e))


class TimelapseErrorHardReset:
    def __init__(self, camera_ctrl_service: CameraCtrlService):
        self._camera_ctrl_service = camera_ctrl_service

    def run(self, **kwargs):
        settings = SettingsFacade()
        if not settings.hard_reset_on_timelapse_error:
            return

        logging.info('Hard resetting')
        try:
            seconds = settings.seconds_to_wait_after_hard_reset
            self._camera_ctrl_service.hard_reset_all_cameras(wait_seconds_after_reset=seconds)
        except Exception as e:
            logging.warning("Hard resetting has failed. Probably it's not supported: {}".format(e))