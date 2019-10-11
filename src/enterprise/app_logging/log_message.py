from datetime import datetime
from enum import Enum


class LogType(Enum):
    INFO = 'INFO'
    ERROR = 'ERROR'


class LogMessage:
    def __init__(
            self,
            *,
            log_type: LogType,
            category: str,
            title: str,
            content: str,
            created_time: datetime):

        self.log_type = log_type
        self.category = category
        self.title = title
        self.content = content
        self.created_time = created_time