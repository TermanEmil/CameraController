from adapters.camera import ctrl
from camera_ctrl.models.app_settings_models import GeneralSettings


class CameraCtrlSettings(ctrl.CameraCtrlSettings):
    @property
    def seconds_to_wait_after_hard_reset(self) -> int:
        return GeneralSettings.get().seconds_to_wait_after_hard_reset

    @property
    def autodetect_cameras_on_start(self) -> bool:
        return GeneralSettings.get().autodetect_cameras_on_start

