class TimelapseSettings:
    @property
    def hard_reset_on_timelapse_error(self) -> bool:
        raise NotImplementedError()

    @property
    def numbers_of_failures_to_reboot_after(self) -> int:
        """If it's a positive number, the it will reboot"""
        raise NotImplementedError()

