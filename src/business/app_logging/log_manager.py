from business.app_logging.log_repository import LogRepository
from enterprise.app_logging.log_message import LogMessage


class LogManager:
    def __init__(self, log_repository: LogRepository):
        self._log_repository = log_repository

    def persistence_log(self, log_message: LogMessage):
        self._log_repository.add(log_message)