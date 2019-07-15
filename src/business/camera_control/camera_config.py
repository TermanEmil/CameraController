from abc import ABC


class CameraConfig:
    @property
    def sections(self) -> dict:
        raise NotImplementedError()

    @property
    def all_fields(self) -> dict:
        raise NotImplementedError()


class CameraConfigWidget:
    def __init__(self, name, label, is_readonly):
        self._name = name
        self._label = label
        self._is_readonly = is_readonly

    @property
    def name(self) -> str:
        return self._name

    @property
    def label(self) -> str:
        return self._label

    @property
    def is_readonly(self) -> str:
        return self._is_readonly


class CameraConfigSection(CameraConfigWidget):
    @property
    def fields(self) -> dict:
        raise NotImplementedError()


class CameraConfigField(CameraConfigWidget):
    @property
    def value(self):
        raise NotImplementedError()

    def set_value(self, value) -> bool:
        # Return True if changed
        raise NotImplementedError()


class CameraConfigChoiceField(CameraConfigField, ABC):
    @property
    def choices(self) -> iter:
        raise NotImplementedError()


class CameraConfigTextField(CameraConfigField, ABC):
    pass


class CameraConfigToggleField(CameraConfigField, ABC):
    pass


class CameraConfigRangeField(CameraConfigField, ABC):
    @property
    def range_min(self):
        raise NotImplementedError()

    @property
    def range_max(self):
        raise NotImplementedError()