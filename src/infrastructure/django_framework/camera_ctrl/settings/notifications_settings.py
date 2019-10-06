from adapters import file_transfer, scheduling
from camera_ctrl.models.app_settings_models import GeneralSettings


class NotificationsSettings(file_transfer.NotificationsSettings, scheduling.NotificationsSettings):
    @property
    def email_log_on_timelapse_error(self) -> bool:
        return GeneralSettings.get().send_email_on_timelapse_error

    @property
    def persistent_log_on_file_transferred(self) -> bool:
        return True

    @property
    def persistent_log_on_capture_taken(self) -> bool:
        return GeneralSettings.get().log_to_db_camera_capture

    @property
    def persistent_log_on_capture_error(self) -> bool:
        return True

    @property
    def email_log_on_capture_error(self) -> bool:
        return GeneralSettings.get().send_email_on_capture_error
