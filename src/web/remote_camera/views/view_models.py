from business.CameraWrapper import CameraWrapper, CameraConfig
from ..forms import CameraConfigSectionForm


class CameraViewModel:
    def __init__(self, camera):
        assert isinstance(camera, CameraWrapper)

        self.name = camera.name
        self.port = camera.port
        self.summary = camera.serial_nb


class CameraConfigSectionViewModel:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly

        self.form = CameraConfigSectionForm(config)


class CameraConfigElement:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly
        self.config_type = config.config_type.name.capitalize()

        self.value = str(config.value)







