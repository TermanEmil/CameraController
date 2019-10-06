from adapters import scheduling
from camera_ctrl.models.app_settings_models import GeneralSettings


class TimelapseSettings(scheduling.TimelapseSettings):
    @property
    def hard_reset_on_timelapse_error(self) -> bool:
        return GeneralSettings.get().hard_reset_on_timelapse_error
