import logging
from datetime import datetime

from adapters.emailing.email_service import EmailService
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType


class FileTransferErrorListener:
    def __init__(self, log_manager: LogManager, email_service: EmailService):
        self._log_manager = log_manager
        self._email_service = email_service

    def run(self, error: str, **kwargs):
        msg = 'Failed to transfer files: {}'.format(error)

        logging.error(msg)
        self._persistent_log(msg)
        self._send_email_log(msg)

    def _persistent_log(self, msg):
        log_message = LogMessage(
            log_type=LogType.ERROR,
            category='FileTransfer',
            title='File transfer failed',
            content=msg,
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)

    def _send_email_log(self, msg):
        subject = 'File transfer failed'

        try:
            self._email_service.send_email(subject=subject, message=msg)

        except Exception as e:
            logging.error('Failed to send emails. Error: {}'.format(e))