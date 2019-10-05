from business.app_logging import log_repository
from camera_ctrl.models import HistoryUnit
from enterprise.app_logging.log_message import LogMessage


class LogRepository(log_repository.LogRepository):
    def add(self, log_message: LogMessage):
        history_unit = HistoryUnit()
        history_unit.log_type = str(log_message.log_type)
        history_unit.category = log_message.category
        history_unit.title = log_message.title
        history_unit.content = log_message.content
        history_unit.created_time = log_message.created_time