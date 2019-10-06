import logging
from typing import Iterable

from adapters.app_logging.email_logger import EmailLogger
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from adapters.emailing.email_service import EmailService
from adapters.scheduling.notifications_settings import NotificationsSettings
from adapters.scheduling.timelapse_settings import TimelapseSettings
from enterprise.camera_ctrl.camera import Camera
from enterprise.scheduling.timelapse import Timelapse
from ._format_capture_error_msg import format_capture_error_msg


def _get_error_msgs(errors: Iterable[dict]) -> Iterable[str]:
    for error in errors:
        camera: Camera = error['camera']
        error_msg: str = error['error']

        yield format_capture_error_msg(camera=camera, error=error_msg)


def _get_log_msg(timelapse: Timelapse, errors: Iterable[dict]) -> str:
    msg = '--- {}: finished with errors. Capture index = {}'.format(timelapse.name, timelapse.capture_index)
    msg += '\n'
    msg += '\n'.join(_get_error_msgs(errors))
    return msg


class TimelapseErrorListener(EmailLogger):
    title = 'Timelapse failed'

    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            timelapse_settings: TimelapseSettings,
            email_service: EmailService,
            camera_ctrl_service: CameraCtrlService):

        super().__init__(email_service)
        self._settings = notifications_settings
        self._timelapse_settings = timelapse_settings
        self._email_service = email_service
        self._camera_ctrl_service = camera_ctrl_service

    def run(self, timelapse: Timelapse, errors: Iterable[dict], **kwargs):
        msg = _get_log_msg(timelapse, errors)

        if self._settings.email_log_on_timelapse_error:
            self.email_log(msg)

        if self._timelapse_settings.hard_reset_on_timelapse_error:
            self._hard_reset()

    def _hard_reset(self):
        logging.info('Hard resetting')
        try:
            self._camera_ctrl_service.hard_reset_all_cameras()
            logging.info('Hard reset - done')

        except Exception as e:
            logging.warning("Hard resetting has failed: {}".format(e))