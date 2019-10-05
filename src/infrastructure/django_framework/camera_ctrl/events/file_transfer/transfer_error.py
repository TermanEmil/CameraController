import logging
from datetime import datetime

from adapters.emailing.email_service import EmailService
from business.app_logging.log_manager import LogManager
from enterprise.app_logging.log_message import LogMessage, LogType


def get_log_msg(error: str):
    return 'Failed to transfer files: {}'.format(error)


def transfer_error_log(error: str, **kwargs):
    logging.error(get_log_msg(error))


class TransferErrorPersistentLog:
    def __init__(self, log_manager: LogManager):
        self._log_manager = log_manager

    def run(self, error: str, **kwargs):
        log_message = LogMessage(
            log_type=LogType.ERROR,
            category='FileTransfer',
            title='File transfer failed',
            content=get_log_msg(error),
            created_time=datetime.utcnow())
        self._log_manager.persistence_log(log_message)


class TransferErrorSendEmail:
    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    def run(self, error: str, **kwargs):
        subject = 'File transfer failed'
        message = get_log_msg(error)

        try:
            self._email_service.send_email(subject=subject, message=message)

        except Exception as e:
            logging.error('Failed to send emails. Error: {}'.format(e))