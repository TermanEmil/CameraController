import logging

from adapters.emailing.email_service import EmailService


class EmailLogger:
    title = ''

    def __init__(self, email_service: EmailService):
        self._email_service = email_service

    def email_log(self, msg: str):
        try:
            self._email_service.send_email(subject=self.title, message=msg)

        except Exception as e:
            logging.error('Failed to send email: {}'.format(e))
