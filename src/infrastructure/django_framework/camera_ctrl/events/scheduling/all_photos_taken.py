import logging
from datetime import datetime

from business.app_logging.log_manager import LogManager
from camera_ctrl.settings_facade import SettingsFacade
from enterprise.app_logging.log_message import LogMessage, LogType
from enterprise.scheduling.timelapse import Timelapse


def _get_log_msg(timelapse: Timelapse):
    return '--- {}: finished taking pictures. Capture index = {}'.format(timelapse.name, timelapse.capture_index)


def all_photos_taken_log(timelapse: Timelapse, **kwargs):
    logging.info(_get_log_msg(timelapse))


class AllPhotosTakenPersistentLog:
    def __init__(self, log_manager: LogManager, settings_facade: SettingsFacade):
        self._log_manager = log_manager
        self._settings = settings_facade

    def run(self, timelapse: Timelapse, **kwargs):
        if not self._settings.log_to_db_timelapse_capture:
            return

        log_message = LogMessage(
            log_type=LogType.INFO,
            category='Timelapse',
            title='Captures done',
            content=_get_log_msg(timelapse),
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)
