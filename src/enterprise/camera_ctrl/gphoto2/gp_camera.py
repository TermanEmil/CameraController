import re

from threading import Lock
from typing import Optional, Iterable

from .gp_camera_config import *
from .. import camera
import os


class GpCamera(camera.Camera):
    def __init__(self, name, port, gp_camera: gp.Camera):
        self._gp_lock = Lock()

        self._gp_camera = gp_camera
        self._name = name
        self._port = port
        self._serial_nb = None

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self):
        return str(self._port)

    @property
    def serial_nb(self):
        if self._serial_nb is None:
            self._serial_nb = self._get_serial_number()

        return self._serial_nb

    @property
    def summary(self) -> str:
        return 'Port: {0}'.format(self._port)

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
            try:
                config = self._gp_camera.get_single_config(config_name)
            except gp.GPhoto2Error:
                config = None

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

    def set_config(self, config_fields: Iterable[GpCameraConfigField]):
        with self._gp_lock:
            for field in config_fields:
                self._gp_camera.set_single_config(field.name, field.gp_widget)

    def capture_preview(self) -> memoryview:
        with self._gp_lock:
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self._gp_camera))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))

        return memoryview(file_data)

    def capture_img(self, storage_dir, filename_prefix) -> str:
        if not os.path.isdir(storage_dir):
            raise Exception('Path: "{0}" does not exist'.format(storage_dir))

        self.disconnect()

        with self._gp_lock:
            file_device_path = gp.check_result(gp.gp_camera_capture(self._gp_camera, gp.GP_CAPTURE_IMAGE))

            _, file_extension = os.path.splitext(file_device_path.name)
            file_extension = file_extension[1:]
            filename = '{0}.{1}'.format(filename_prefix, file_extension)
            file_path = os.path.join(storage_dir, filename)

            camera_file = gp.check_result(
                gp.gp_camera_file_get(
                    self._gp_camera,
                    file_device_path.folder,
                    file_device_path.name,
                    gp.GP_FILE_TYPE_NORMAL))
            gp.check_result(gp.gp_file_save(camera_file, file_path))

        return file_path

    def _get_serial_number(self):
        with self._gp_lock:
            summary = gp.check_result(gp.gp_camera_get_summary(self._gp_camera))

        cam_summary = summary.text
        m = re.search(r'serial\s*number\s*[:=]?\s*0*(\d+)', cam_summary, flags=re.IGNORECASE)
        if m:
            return int(m.group(1))

        raise Exception('Could not extract the serial number')
