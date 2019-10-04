import logging

from camera_ctrl.log_to_db import LogType, log_to_db
from enterprise.scheduling.timelapse import Timelapse
from proj_settings.settings_facade import SettingsFacade


def _get_log_msg(timelapse: Timelapse):
    return '--- {}: finished taking pictures. Capture index = {}'.format(timelapse.name, timelapse.capture_index)


def all_photos_taken_log(timelapse: Timelapse, **kwargs):
    logging.info(_get_log_msg(timelapse))


def all_photos_taken_log_to_db(timelapse: Timelapse, **kwargs):
    settings = SettingsFacade()
    if not settings.log_to_db_timelapse_capture:
        return

    log_type = LogType.INFO
    category = 'Timelapse'
    title = 'Captures done'
    content = _get_log_msg(timelapse)

    log_to_db(log_type=log_type, category=category, title=title, content=content)