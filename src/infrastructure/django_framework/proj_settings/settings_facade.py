from typing import Iterable

from proj_settings.models import GeneralSettings


class SettingsFacade:
    @property
    def send_email_on_error(self) -> bool:
        return GeneralSettings.get().send_email_on_error

    @property
    def log_to_db_timelapse_capture(self) -> bool:
        return GeneralSettings.get().log_to_db_timelapse_capture

    @property
    def log_to_db_camera_capture(self) -> bool:
        return GeneralSettings.get().log_to_db_camera_capture

    @property
    def autodetect_cameras_on_start(self) -> bool:
        return GeneralSettings.get().autodetect_cameras_on_start

    @property
    def emails(self) -> Iterable[str]:
        return GeneralSettings.get().emails.split()
