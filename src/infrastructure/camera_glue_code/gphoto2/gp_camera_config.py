from textwrap import shorten
from typing import Tuple

import gphoto2 as gp

from enterprise.camera_ctrl.camera_config import CameraConfig, CameraConfigSection, CameraConfigField, \
    CameraConfigTextField, CameraConfigChoiceField, CameraConfigToggleField, CameraConfigRangeField
from enterprise.camera_ctrl.exceptions import InvalidConfigException, ConfigIsReadonlyException, \
    NotAValidChoiceForConfigException


class GpCameraConfig(CameraConfig):
    def __init__(self, gp_widget: gp.CameraWidget):
        self._gp_widget = gp_widget

        if gp_widget.count_children() <= 0:
            return

        raw_sections = gp_widget.get_children()
        if raw_sections is None:
            raise Exception('Failed to extract the configs')

        self._sections = {}
        self._all_fields = {}
        for raw_section in raw_sections:
            section = GpCameraConfigSection(raw_section)
            self._sections[section.name] = section
            self._all_fields.update(section.fields)

    @property
    def sections(self) -> dict:
        return self._sections

    @property
    def all_fields(self) -> dict:
        return self._all_fields


class GpCameraConfigSection(CameraConfigSection):
    def __init__(self, gp_widget: gp.CameraWidget):
        name = gp_widget.get_name()
        label = gp_widget.get_label()
        is_readonly = (gp_widget.get_readonly() != 0)

        super().__init__(name, label, is_readonly)

        self._fields = {}
        raw_fields = gp_widget.get_children()

        if raw_fields is None:
            return

        for raw_field in raw_fields:
            field = build_config_field(raw_field)
            if field is not None:
                self._fields[field.name] = field

    @property
    def fields(self):
        return self._fields


def build_config_field(gp_widget: gp.CameraWidget):
    config_type = gp_widget.get_type()

    if config_type == gp.GP_WIDGET_TEXT:
        return GpCameraConfigTextField(gp_widget)

    if config_type == gp.GP_WIDGET_RANGE:
        return GpCameraConfigRangeField(gp_widget)

    if config_type == gp.GP_WIDGET_TOGGLE:
        return GpCameraConfigToggleField(gp_widget)

    if config_type == gp.GP_WIDGET_RADIO or config_type == gp.GP_WIDGET_MENU:
        return GpCameraConfigChoiceField(gp_widget)

    return None


class GpCameraConfigField(CameraConfigField):
    def __init__(self, gp_widget: gp.CameraWidget):
        name = gp_widget.get_name()
        label = gp_widget.get_label()
        is_readonly = (gp_widget.get_readonly() != 0)

        super().__init__(name, label, is_readonly)
        self._value = gp_widget.get_value()
        self.gp_widget = gp_widget

    @property
    def value(self):
        return self._value

    def set_value(self, value):
        if self.is_readonly:
            raise ConfigIsReadonlyException()

        if self.value == value:
            return

        self._value = value
        self.gp_widget.set_value(value)


class GpCameraConfigTextField(GpCameraConfigField, CameraConfigTextField):
    def set_value(self, value):
        value = shorten(value, 256)

        if (len(value) == 0 or value.isspace()) and self.value.isspace():
            value = self.value

        super().set_value(value)


class GpCameraConfigChoiceField(GpCameraConfigField, CameraConfigChoiceField):
    def __init__(self, gp_widget: gp.CameraWidget):
        super().__init__(gp_widget)
        self._choices = list(self._get_choices())
        self._fix_choices()

    @property
    def choices(self) -> iter:
        return self._choices

    def set_value(self, value):
        if value not in self._choices:
            raise NotAValidChoiceForConfigException(self.choices)

        super().set_value(value)

    def _get_choices(self):
        for choice in self.gp_widget.get_choices():
            if not choice:
                continue

            yield str(choice)

    def _fix_choices(self):
        # Sometimes, the initial value is not from the choice list.
        if self.value is None or self.value not in self.choices:
            self._choices.append(str(self.value))


class GpCameraConfigToggleField(GpCameraConfigField, CameraConfigToggleField):
    def set_value(self, value):
        try:
            parsed_value = bool(value)
        except ValueError:
            raise InvalidConfigException('Expected boolean value')

        if parsed_value != bool(self.value):
            super().set_value(int(value))


class GpCameraConfigRangeField(GpCameraConfigField, CameraConfigRangeField):
    def __init__(self, gp_widget: gp.CameraWidget):
        super().__init__(gp_widget)
        self._range_min, self._range_max, self._inc = self._get_ranges()

    @property
    def range_min(self):
        return self._range_min

    @property
    def range_max(self):
        return self._range_max

    def set_value(self, value):
        try:
            parsed_value = float(value)
        except ValueError:
            raise InvalidConfigException('Expected float value')

        if parsed_value < self.range_min or parsed_value > self.range_max:
            raise InvalidConfigException(f'Value not withing [{self.range_min}; {self.range_max}]')

        super().set_value(value)

    def _get_ranges(self) -> Tuple[float, float, float]:
        return self.gp_widget.get_range()