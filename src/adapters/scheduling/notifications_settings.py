class NotificationsSettings:
    @property
    def persistent_log_on_capture_taken(self) -> bool:
        raise NotImplementedError()

    @property
    def persistent_log_on_capture_error(self) -> bool:
        raise NotImplementedError()

    @property
    def email_log_on_capture_error(self) -> bool:
        raise NotImplementedError()

    @property
    def email_log_on_timelapse_error(self) -> bool:
        raise NotImplementedError()
