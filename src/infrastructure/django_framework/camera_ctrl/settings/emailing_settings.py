from typing import Iterable

from adapters import emailing
from camera_ctrl.models.app_settings_models import GeneralSettings


class EmailingSettings(emailing.EmailingSettings):
    @property
    def emails(self) -> Iterable[str]:
        return GeneralSettings.get().emails.split()

    @property
    def email_subject_prefix(self) -> str:
        return GeneralSettings.get().email_subject_prefix
