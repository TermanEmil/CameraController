from typing import Iterable


class InvalidConfigException(Exception):
    def __init__(self, message):
        super().__init__(f'Invalid config: {message}')


class ConfigIsReadonlyException(InvalidConfigException):
    def __init__(self):
        super().__init__('It is readonly')


class NotAValidChoiceForConfigException(InvalidConfigException):
    def __init__(self, choices: Iterable[str]):
        super().__init__('Config must be one of [{}]'.format(', '.join(choices)))
