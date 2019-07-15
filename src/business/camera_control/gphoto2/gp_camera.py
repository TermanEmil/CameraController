import re

from threading import Lock
from typing import Optional

from .gp_camera_config import *
from .. import camera


class GpCamera(camera.Camera):
    def __init__(self, name, port, gp_camera: gp.Camera, gp_lock: Lock):
        self._gp_lock = gp_lock

        self._gp_camera = gp_camera
        self._name = name
        self._port = port
        # self._serial_nb = self._get_serial_number()
        self._serial_nb = 'fuck'

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self):
        return str(self._port)

    @property
    def summary(self) -> str:
        return 'Port: {1}'.format(self._serial_nb, self._port)

    def disconnect(self):
        with self._gp_lock:
            self._gp_camera.exit()
            print('Disconnected from {0} ID: {1} Port: {2}'.format(self.name, self.id, self._port))

    def list_configs(self) -> iter:
        with self._gp_lock:
            config_names = self._gp_camera.list_config()

        return [config_name[0] for config_name in config_names]

    def get_single_config(self, config_name) -> Optional[CameraConfigField]:
        with self._gp_lock:
            config = self._gp_camera.get_single_config(config_name)

        if config is None:
            return None

        return build_config_field(config)

    def get_config(self) -> CameraConfig:
        with self._gp_lock:
            camera_config_widget = self._gp_camera.get_config()
            if camera_config_widget is None:
                raise Exception('Could not extract the configurations')

            config = GpCameraConfig(camera_config_widget)

        return config

    def set_config(self, config_fields: iter):
        with self._gp_lock:
            for field in config_fields:
                assert isinstance(field, GpCameraConfigField)
                self._gp_camera.set_single_config(field.name, field.gp_widget)

    def capture_preview(self) -> memoryview:
        with self._gp_lock:
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self._gp_camera))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

        return memoryview(file_data)

    def _get_serial_number(self):
        with self._gp_lock:
            summary = gp.check_result(gp.gp_camera_get_summary(self._gp_camera))

        cam_summary = summary.text
        m = re.search(r'serial\s*number\s*[:=]?\s*0*(\d+)', cam_summary, flags=re.IGNORECASE)
        if m:
            return int(m.group(1))

        raise Exception('Could not extract the serial number')