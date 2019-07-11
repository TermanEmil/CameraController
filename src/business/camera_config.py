from enum import Enum
import gphoto2 as gp


# Everything must be loaded from the start, because the widgets magically disappear from memory.
class CameraConfig:
    def __init__(self, camera, gp_sync):
        # gp_sync must be a lock
        assert isinstance(camera, gp.Camera)

        self._camera = camera
        self._gp_sync = gp_sync
        self.sections = []

        with self._gp_sync:
            camera_config = self._camera.get_config()
            if camera_config.count_children() <= 0:
                return

            raw_sections = camera_config.get_children()
            if raw_sections is None:
                raise Exception('Failed to extract the configs')

            self.sections = [CameraConfigSection(section_widget) for section_widget in raw_sections]


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

        raw_elements = section_widget.get_children()
        if raw_elements:
            self.fields = [CameraConfigField(field, self) for field in raw_elements]
        else:
            self.fields = []


class CameraConfigField(CameraConfigWidget):
    def __init__(self, element_widget, parent_widget):
        assert isinstance(element_widget, gp.CameraWidget)
        assert isinstance(parent_widget, CameraConfigWidget)
        super().__init__(element_widget)

        self.parent_widget = parent_widget
        self._config = element_widget

        self.config_type = CameraConfigType(self._config.get_type())
        self.value = self._config.get_value()
        self.choices = self._get_choices()
        self.range_min, self.range_max, inc = self._get_range()

    def get_key(self):
        return 'config/{0}/{1}'.format(self.parent_widget.name, self.name)

    def _get_choices(self):
        if self.config_type != CameraConfigType.RADIO and self.config_type != CameraConfigType.MENU:
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
