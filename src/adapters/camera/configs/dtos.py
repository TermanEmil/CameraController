from enum import Enum
from typing import Iterable


class ConfigFieldType(Enum):
    CHOICE = 0
    TEXT = 1
    TOGGLE = 2
    RANGE = 3
    UNDEFINED = 4


class Range:
    def __init__(self, min_val: float, max_val: float):
        self.min_val = min_val
        self.max_val = max_val


class ConfigFieldDto:
    field_type: ConfigFieldType
    value: str
    is_readonly: bool
    name: str
    label: str
    choices: Iterable[str]
    val_range: Range

    def __init__(
            self,
            field_type: ConfigFieldType,
            value: str,
            is_readonly: bool,
            name: str,
            label: str,
            choices: Iterable[str] = None,
            val_range: Range = None):

        self.field_type = field_type
        self.value = value
        self.is_readonly = is_readonly
        self.name = name
        self.label = label
        self.choices = choices
        self.val_range = val_range


class ConfigSectionDto:
    def __init__(self, name: str, label: str, fields: Iterable[ConfigFieldDto]):
        self.name = name
        self.label = label
        self.fields = list(fields)


class ConfigsDto:
    def __init__(self, sections: Iterable[ConfigSectionDto]):
        self.sections = list(sections)