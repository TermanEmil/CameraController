from business.CameraWrapper import CameraWrapper, CameraConfig
from ..forms import CameraConfigForm


class CameraViewModel:
    def __init__(self, camera):
        assert isinstance(camera, CameraWrapper)

        self.name = camera.name
        self.port = camera.port
        self.summary = camera.serial_nb


class CameraConfigViewModel:
    def __init__(self, configs):
        self.sections = []
        self.form_fields = {}
        for config in configs:
            section = CameraConfigSectionViewModel(config)

            self.sections.append(section)
            self.form_fields.update(section.form_fields)


class CameraConfigSectionViewModel:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly

        self.form_fields = CameraConfigForm.extract_fields_for_camera_config_section(config)


class CameraConfigElement:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly
        self.config_type = config.config_type.name.capitalize()

        self.value = str(config.value)







