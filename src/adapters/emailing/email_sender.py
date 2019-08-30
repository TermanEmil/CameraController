from typing import Iterable


class EmailSender:
    def send_email(self, subject: str, message: str, to_emails=Iterable[str]):
        raise NotImplementedError()