from typing import Iterable

from django.core.mail import send_mail

from adapters.emailing.email_sender import EmailSender


class DjangoEmailSender(EmailSender):
    def send_email(self, subject: str, message: str, to_emails=Iterable[str]):
        send_mail(
            subject=subject,
            message=message,
            from_email=None,
            recipient_list=list(to_emails),
            fail_silently=False)