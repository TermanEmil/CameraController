import logging
from datetime import datetime

from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType


def get_log_msg(file: str):
    return '{}: has been transferred'.format(file)


def file_transferred_log(file: str, **kwargs):
    logging.info(get_log_msg(file))


class FileTransferPersistentLog:
    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def run(self, file: str, **kwargs):
        log_message = LogMessage(
            log_type=LogType.INFO,
            category='FileTransfer',
            title='File transferred',
            content=get_log_msg(file),
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)
