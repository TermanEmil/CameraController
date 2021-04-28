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


class InvalidConfigException(CameraException):
    def __init__(self, config_name: str, details: str = None):
        msg = f'Invalid config for {config_name}'
        if details:
            msg += f': {details}'
        super().__init__(msg)


class CameraResetException(Exception):
    def __init__(self, msg):
        super().__init__('Camera reset failed: {}'.format(msg))


class CameraResetNotSupportedException(CameraResetException):
    def __init__(self, msg):
        super().__init__('Camera reset not supported: {}'.format(msg))