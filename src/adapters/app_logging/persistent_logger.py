from datetime import datetime

from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType


class PersistentLogger:
    log_type = LogType.INFO
    category = ''
    title = ''

    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def persistent_log(self, msg: str):
        log_message = LogMessage(
            log_type=self.log_type,
            category=self.category,
            title=self.title,
            content=msg,
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)