from enterprise.app_logging.log_message import LogMessage


class LogRepository:
    def add(self, log_message: LogMessage):
        raise NotImplementedError()