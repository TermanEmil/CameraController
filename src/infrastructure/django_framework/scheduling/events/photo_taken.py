from enterprise.camera_ctrl.camera import Camera
import logging

from proj_logging.internal_api.log_to_db import LogType, log_to_db
from proj_settings.settings_facade import SettingsFacade


def _get_log_msg(camera: Camera, filepath: str):
    return 'Camera {}: Photo taken to {}'.format(camera.name, filepath)


def photo_taken_log(camera: Camera, filepath: str, **kwargs):
    logging.info(_get_log_msg(camera, filepath))


def photo_taken_log_to_db(camera: Camera, filepath: str, **kwargs):
    settings = SettingsFacade()
    if not settings.log_to_db_camera_capture:
        return

    log_type = LogType.INFO
    category = 'Timelapse'
    title = 'Photo taken'
    content = _get_log_msg(camera, filepath)

    log_to_db(log_type=log_type, category=category, title=title, content=content)