from business.CameraWrapper import CameraWrapper, CameraConfig


class CameraViewModel:
    def __init__(self, camera):
        assert isinstance(camera, CameraWrapper)

        self.name = camera.name
        self.port = camera.port
        self.summary = camera.serial_nb


class CameraConfigSection:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly

        self.elements = [CameraConfigElement(element) for element in config.child_configs]


class CameraConfigElement:
    def __init__(self, config):
        assert isinstance(config, CameraConfig)

        self.name = config.name
        self.label = config.label
        self.is_readonly = config.is_readonly
        self.config_type = config.config_type.name.capitalize()

        self.value = str(config.value)







