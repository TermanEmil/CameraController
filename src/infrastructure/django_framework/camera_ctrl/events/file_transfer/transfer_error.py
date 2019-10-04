import logging

from adapters.emailing.email_service import EmailService
from camera_ctrl.log_to_db import LogType, log_to_db


def get_log_msg(error: str):
    return 'Failed to transfer files: {}'.format(error)


def transfer_error_log(error: str, **kwargs):
    logging.error(get_log_msg(error))


def transfer_error_log_to_db(error: str, **kwargs):
    log_type = LogType.ERROR
    category = 'FileTransfer'
    title = 'File transfer failed'
    content = get_log_msg(error)

    log_to_db(log_type=log_type, category=category, title=title, content=content)


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