import logging

from enterprise.scheduling.timelapse import Timelapse


def _get_log_msg(timelapse: Timelapse):
    return '--- {}: finished taking pictures. Capture index = {}'.format(timelapse.name, timelapse.capture_index)


def all_photos_taken_log(timelapse: Timelapse, **kwargs):
    logging.info(_get_log_msg(timelapse))
