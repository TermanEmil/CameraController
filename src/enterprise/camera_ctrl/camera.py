from threading import Lock
from typing import Iterable

from .camera_config import CameraConfig, CameraConfigField


class Camera:
    @property
    def sync_lock(self) -> Lock:
        raise NotImplementedError()

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @property
    def id(self):
        raise NotImplementedError()

    @property
    def serial_nb(self):
        raise NotImplementedError()

    @property
    def summary(self) -> str:
        raise NotImplementedError()

    def list_configs(self) -> Iterable[str]:
        # List all the available camera_config names
        raise NotImplementedError()

    def get_single_config(self, config_name) -> CameraConfigField:
        raise NotImplementedError()

    def get_config(self) -> CameraConfig:
        raise NotImplementedError()

    def set_config(self, config_fields: Iterable[CameraConfigField]):
        raise NotImplementedError()

    def capture_preview(self) -> memoryview:
        raise NotImplementedError()

    def capture_img(self, storage_dir, filename_prefix) -> str:
        raise NotImplementedError()

    def disconnect(self):
        raise NotImplementedError()