from enum import Enum
import gphoto2 as gp
from .utils.math_utils import clamp
from textwrap import shorten


# Everything must be loaded from the start, because the widgets magically disappear from the memory.
class CameraConfig:
    def __init__(self, camera, gp_sync):
        # gp_sync must be a lock
        assert isinstance(camera, gp.Camera)

        self._camera = camera
        self._gp_sync = gp_sync
        self.sections = []
        self.all_fields_dict = {}

        with self._gp_sync:
            self.gp_config = self._camera.get_config()
            if self.gp_config.count_children() <= 0:
                return

            raw_sections = self.gp_config.get_children()
            if raw_sections is None:
                raise Exception('Failed to extract the configs')

            for raw_section in raw_sections:
                section = CameraConfigSection(raw_section)
                self.sections.append(section)
                self.all_fields_dict.update(section.fields_dict)

    def set_values(self, values_dict):
        i = 0
        with self._gp_sync:
            for key, value in values_dict.items():
                if value is None:
                    continue

                field = self.all_fields_dict.get(key)
                if field is None:
                    continue

                assert isinstance(field, CameraConfigField)

                value = field.parse_value(value)
                if field.is_readonly or field.value == value:
                    continue

                if key == 'config/other/5011':
                    continue

                print("'{0}' -> '{1}' {2}".format(field.value, value, field.get_key()))
                field.set_value(value)
                self._camera.set_single_config(field.name, field._config)


class CameraConfigWidget:
    def __init__(self, camera_widget):
        assert isinstance(camera_widget, gp.CameraWidget)

        self.name = camera_widget.get_name()
        self.label = camera_widget.get_label()
        self.is_readonly = (camera_widget.get_readonly() != 0)


class CameraConfigSection(CameraConfigWidget):
    def __init__(self, section_widget):
        assert isinstance(section_widget, gp.CameraWidget)
        super().__init__(section_widget)

        self.fields_dict = {}

        raw_fields = section_widget.get_children()
        if raw_fields:
            for raw_field in raw_fields:
                field = CameraConfigField(raw_field, self)
                self.fields_dict[field.get_key()] = field


class CameraConfigField(CameraConfigWidget):
    def __init__(self, element_widget, parent_widget):
        assert isinstance(element_widget, gp.CameraWidget)
        assert isinstance(parent_widget, CameraConfigWidget)
        super().__init__(element_widget)

        self.parent_widget = parent_widget
        self._config = element_widget

        self.config_type = CameraConfigType(self._config.get_type())
        self.range_min, self.range_max, inc = self._get_range()
        self.choices = self._get_choices()
        self.value = self._get_value()

        # I don't have time to process the bugs of this useless option.
        if self.config_type == CameraConfigType.DATE:
            self.is_readonly = True

        self._fix_choices()

    def get_key(self):
        return 'config/{0}/{1}'.format(self.parent_widget.name, self.name)

    def set_value(self, value):
        if self.is_multichoice() and value not in self.choices:
            raise Exception('Value is not in the choice list')

        if self.config_type == CameraConfigType.RANGE:
            value = str(clamp(float(value), self.range_min, self.range_max))

        if self.config_type == CameraConfigType.TEXT:
            value = shorten(value, 256)

        self.value = value
        self._config.set_value(value)

    def is_multichoice(self):
        return self.config_type == CameraConfigType.RADIO or self.config_type == CameraConfigType.MENU

    def parse_value(self, value):
        if self.config_type == CameraConfigType.TOGGLE:
            # The toggle value is stored as an int. Nb 2 is considered True
            assert isinstance(value, bool)

            if bool(self.value) == value:
                return self.value
            else:
                return int(value)

        if self.config_type == CameraConfigType.TEXT:
            # Some text fields have weird spaces
            assert isinstance(value, str)

            if (len(value) == 0 or value.isspace()) and self.value.isspace():
                return self.value

        return value

    def _get_value(self):
        value = self._config.get_value()

        if self.config_type == CameraConfigType.TEXT:
            if value is None:
                return ''

        return value

    def _fix_choices(self):
        # Sometimes, the value is not one from the list of choices.
        if self.choices is None:
            return

        if self.value is None or self.value not in self.choices:
            self.choices.append(str(self.value))
            return

    def _get_choices(self):
        if not self.is_multichoice():
            return None

        choices = []
        for choice in self._config.get_choices():
            if not choice:
                continue

            choices.append(str(choice))
        return choices

    def _get_range(self):
        if self.config_type != CameraConfigType.RANGE:
            return None, None, None

        return self._config.get_range()


class CameraConfigType(Enum):
    SECTION = gp.GP_WIDGET_SECTION
    TEXT = gp.GP_WIDGET_TEXT
    RANGE = gp.GP_WIDGET_RANGE
    TOGGLE = gp.GP_WIDGET_TOGGLE
    RADIO = gp.GP_WIDGET_RADIO
    MENU = gp.GP_WIDGET_MENU
    DATE = gp.GP_WIDGET_DATE
