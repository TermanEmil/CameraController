from typing import Iterable

from proj_settings.models import GeneralSettings


class SettingsFacade:
    @property
    def send_email_on_capture_error(self) -> bool:
        return GeneralSettings.get().send_email_on_capture_error

    @property
    def send_email_on_timelapse_error(self) -> bool:
        return GeneralSettings.get().send_email_on_timelapse_error

    @property
    def send_email_on_sync_error(self) -> bool:
        return GeneralSettings.get().send_email_on_sync_error

    @property
    def seconds_to_wait_after_hard_reset(self) -> int:
        return GeneralSettings.get().seconds_to_wait_after_hard_reset

    @property
    def hard_reset_on_timelapse_error(self) -> bool:
        return GeneralSettings.get().hard_reset_on_timelapse_error

    @property
    def log_to_db_timelapse_capture(self) -> bool:
        return GeneralSettings.get().log_to_db_timelapse_capture

    @property
    def log_to_db_camera_capture(self) -> bool:
        return GeneralSettings.get().log_to_db_camera_capture

    @property
    def emails(self) -> Iterable[str]:
        return GeneralSettings.get().emails.split()

    @property
    def autodetect_cameras_on_start(self) -> bool:
        return GeneralSettings.get().autodetect_cameras_on_start
