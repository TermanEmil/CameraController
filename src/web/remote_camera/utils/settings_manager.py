import json
from business.camera_wrapper import CameraWrapper


class SettingsManager:
    def __init__(self, session):
        self.session = session

    def get_settings(self, camera):
        assert isinstance(camera, CameraWrapper)

        key = SettingsManager.get_settings_key(camera)
        camera_settings_json = self.session.get(key, None)

        if camera_settings_json is None:
            return CameraSettings.default()
        else:
            return CameraSettings.from_json(json.loads(camera_settings_json))

    def set_settings(self, camera, settings):
        assert isinstance(camera, CameraWrapper)
        assert isinstance(settings, CameraSettings)

        key = SettingsManager.get_settings_key(camera)
        self.session[key] = settings.to_json()

    @staticmethod
    def get_settings_key(camera):
        assert isinstance(camera, CameraWrapper)
        return 'camera_setting_{0}'.format(camera.serial_nb)


class CameraSettings:
    def __init__(self, quality):
        assert 1 <= quality <= 100

        self.quality = quality

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    @classmethod
    def from_json(cls, j):
        return cls(**j)

    @classmethod
    def default(cls):
        return cls(quality=100)
