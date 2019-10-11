import logging
from datetime import datetime

from adapters.file_transfer.notifications_settings import NotificationsSettings
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType


class FileTransferredListener:
    def __init__(
            self,
            notifications_settings: NotificationsSettings,
            log_manager: LogManager):

        self._log_manager = log_manager
        self._notifications_settings = notifications_settings

    def run(self, file: str, **kwargs):
        msg = '{}: has been transferred'.format(file)

        logging.info(msg)
        if self._notifications_settings.persistent_log_on_file_transferred:
            self.persistent_log(msg)

    def persistent_log(self, msg):
        log_message = LogMessage(
            log_type=LogType.INFO,
            category='FileTransfer',
            title='File transferred',
            content=msg,
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)