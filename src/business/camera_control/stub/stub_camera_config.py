from ..camera_config import *


class StubCameraConfig(CameraConfig):
    def __init__(self, sections=None):
        if sections is None:
            sections = {}

        self._sections = sections

    @property
    def sections(self):
        return self._sections

    @property
    def all_fields(self):
        all_fields = {}

        for _, section in self._sections.items():
            assert isinstance(section, CameraConfigSection)
            all_fields.update(section.fields)

        return all_fields


class StubCameraConfigSection(CameraConfigSection):
    def __init__(self, name, label, is_readonly, fields=None):
        super().__init__(name, label, is_readonly)

        if fields is None:
            fields = {}

        self._fields = fields

    @property
    def fields(self):
        return self._fields


class StubCameraConfigField(CameraConfigField):
    def __init__(self, name, label, is_readonly, value):
        super().__init__(name, label, is_readonly)
        self._value = value

    @property
    def value(self):
        return self._value

    def set_value(self, value) -> bool:
        self._value = value
        return True


class StubCameraConfigTextField(StubCameraConfigField, CameraConfigTextField):
    pass


class StubCameraConfigChoiceField(StubCameraConfigField, CameraConfigChoiceField):
    def __init__(self, name, label, is_readonly, value, choices: iter):
        super().__init__(name, label, is_readonly, value)
        self._choices = choices

    @property
    def choices(self) -> iter:
        return self._choices

    def set_value(self, value):
        if value not in self._choices:
            raise Exception('Choice not in list')
        self._value = value


class StubCameraConfigToggleField(StubCameraConfigField, CameraConfigToggleField):
    def set_value(self, value):
        if isinstance(value, bool):
            self._value = int(value)
        else:
            self._value = value


class StubCameraConfigRangeField(StubCameraConfigField, CameraConfigRangeField):
    def __init__(self, name, label, is_readonly, value, range_min, range_max):
        super().__init__(name, label, is_readonly, value)
        self._range_min = range_min
        self._range_max = range_max

    @property
    def range_min(self):
        return self._range_min

    @property
    def range_max(self):
        return self._range_max

    def set_value(self, value):
        self._value = max(min(self.range_max, value), self.range_min)