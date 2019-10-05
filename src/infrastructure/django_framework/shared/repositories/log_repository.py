from business.app_logging import log_repository
from camera_ctrl.models import HistoryUnit
from enterprise.app_logging.log_message import LogMessage


class LogRepository(log_repository.LogRepository):
    def add(self, log_message: LogMessage):
        HistoryUnit.objects.create_from_log_message(log_message)