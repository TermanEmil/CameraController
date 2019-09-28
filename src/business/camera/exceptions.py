class CameraException(Exception):
    def __init__(self, message):
        super().__init__('Camera error: {}'.format(message))


class CameraNotFoundException(CameraException):
    def __init__(self):
        super().__init__('Camera not found')


class ConfigNotFoundException(CameraException):
    def __init__(self, config_name: str = None):
        msg = 'Config not found or not supported'
        if str:
            msg += ': {}'.format(config_name)
        super().__init__(msg)


class HardResetException(Exception):
    def __init__(self, msg):
        super().__init__('Hard reset failed: {}'.format(msg))


class HardResetNotSupportedException(HardResetException):
    def __init__(self, msg):
        super().__init__('Hard reset not supported: {}'.format(msg))