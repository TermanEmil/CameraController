import logging
from enum import Enum

from camera_ctrl.models import HistoryUnit


class LogType(Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'


def log_to_db(*, log_type: LogType, category: str, title: str, content: str):
    try:
        HistoryUnit.objects.create(log_type=log_type.name, category=category, title=title, content=content)
    except Exception as e:
        logging.error('Failed to log to db. Error: {}'.format(e))