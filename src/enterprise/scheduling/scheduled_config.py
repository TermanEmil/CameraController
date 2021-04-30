from typing import List


class Config:
    def __init__(
            self,
            *,
            name: str,
            value: str,
            **kwargs):

        self.name = name
        self.value = value


class ScheduledConfig:
    def __init__(
            self,
            *,
            name: str,
            configs: List[Config],
            **kwargs):

        self.name = name
        self.configs = configs
