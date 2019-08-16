class Timelapse:
    def __init__(
            self,
            *,
            pk: int = None,
            name: str = None,
            storage_dir_format: str = None,
            filename_format: str = None,
            schedule_id=None,
            capture_index: int = 0,
            **kwargs):

        self.pk = pk
        self.name = name
        self.storage_dir_format = storage_dir_format
        self.filename_format = filename_format
        self.schedule_id = schedule_id
        self.capture_index = capture_index
