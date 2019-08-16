class CameraNotFound(Exception):
    def __init__(self):
        super().__init__('Camera not found')


class ConfigNotFound(Exception):
    def __init__(self):
        super().__init__('Config not found or not supported')