from .camera_config import CameraConfig, CameraConfigField


class Camera:
    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def id(self):
        raise NotImplementedError()

    @property
    def summary(self) -> str:
        raise NotImplementedError()

    def list_configs(self) -> iter:
        # List all the available config names
        raise NotImplementedError()

    def get_single_config(self, config_name) -> CameraConfigField:
        raise NotImplementedError()

    def get_config(self) -> CameraConfig:
        raise NotImplementedError()

    def set_config(self, config_fields: iter):
        raise NotImplementedError()

    def capture_preview(self) -> memoryview:
        raise NotImplementedError()

    def capture_img(self, storage_dir, filename_prefix) -> str:
        raise NotImplementedError()
