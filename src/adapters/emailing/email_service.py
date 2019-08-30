from adapters.emailing.email_sender import EmailSender
from adapters.emailing.emailing_settings import EmailingSettings


class EmailService:
    def __init__(self, email_sender: EmailSender, emailing_settings: EmailingSettings):
        self._email_sender = email_sender
        self._emailing_settings = emailing_settings

    def send_email(self, subject: str, message: str):
        emails = list(self._emailing_settings.emails)
        if len(emails) == 0:
            return

        subject = '{} {}'.format(self._emailing_settings.email_subject_prefix, subject)
        self._email_sender.send_email(subject=subject, message=message, to_emails=emails)