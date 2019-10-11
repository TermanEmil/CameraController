class CameraCtrlSettings:
    @property
    def seconds_to_wait_after_hard_reset(self) -> int:
        raise NotImplementedError()

    @property
    def autodetect_cameras_on_start(self) -> bool:
        raise NotImplementedError()