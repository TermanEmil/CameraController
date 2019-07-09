import os
import gphoto2 as gp
import threading
import re
from enum import Enum

from .utils.async_print import async_print


def _extract_serial_number(cam_summary):
    m = re.search(r'serial\s*number\s*[:=]?\s*(\d+)', cam_summary, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))

    return None


class CameraWrapper:
    def __init__(self, gp_camera, storage_dir=None, camera_name=None, port=None):
        assert isinstance(gp_camera, gp.Camera)

        self.gp_camera = gp_camera
        self.storage_dir = storage_dir
        self.name = camera_name
        self.port = port

        self.verbose = True

        summary = gp.check_result(gp.gp_camera_get_summary(self.gp_camera))
        self.serial_nb = _extract_serial_number(summary.text)

        # The gphoto2 operations must synchronized.
        # Weird shit happens if multiple gphoto2 operations on the same camera happen at once.
        self._gp_sync = threading.Lock()

    def capture_img(self, img_index=0):
        assert self.storage_dir is not None

        if not os.path.isdir(self.storage_dir):
            raise Exception('Path: "{0}" does not exist'.format(self.storage_dir))

        self._log('Capturing image')
        with self._gp_sync:
            file_device_path = gp.check_result(gp.gp_camera_capture(self.gp_camera, gp.GP_CAPTURE_IMAGE))

        photo_name = self._create_img_name(file_device_path.name, img_index)
        local_file_path = os.path.join(self.storage_dir, photo_name)

        with self._gp_sync:
            camera_file = gp.check_result(
                gp.gp_camera_file_get(
                    self.gp_camera,
                    file_device_path.folder,
                    file_device_path.name,
                    gp.GP_FILE_TYPE_NORMAL))
            gp.check_result(gp.gp_file_save(camera_file, local_file_path))
        self._log('Image saved to {0}'.format(local_file_path))

    def capture_preview(self):
        with self._gp_sync:
            camera_file = gp.check_result(gp.gp_camera_capture_preview(self.gp_camera))
            file_data = gp.check_result(gp.gp_file_get_data_and_size(camera_file))
        data = memoryview(file_data)

        return data

    def get_config(self):
        with self._gp_sync:
            camera_configs = self.gp_camera.get_config()

            if camera_configs.count_children() < 1:
                raise Exception('Failed to extract the configs')

            children = camera_configs.get_children()

        return [CameraConfig(child, self._gp_sync) for child in children]

    def disconnect(self):
        with self._gp_sync:
            self.gp_camera.exit()
        self._log('Disconnected')

    def _log(self, text):
        if self.verbose:
            async_print('{0}: {1}'.format(self.name, text))

    def _create_img_name(self, device_img_name, img_index):
        file_name, file_extension = os.path.splitext(device_img_name)

        # Without the dot
        file_extension = file_extension[1:]
        return '{0}-{1}.{2}'.format(self.name, img_index, file_extension)


class CameraConfig:
    def __init__(self, config, gp_sync):
        self._config = config
        self._gp_sync = gp_sync

        with self._gp_sync:
            self.label = config.get_label()
            self.name = config.get_name()
            self.config_type = CameraConfigType(config.get_type())
            self.is_readonly = (config.get_readonly() != 0)
            self.value = self._get_value()

            self.choices = self._get_choices()
            a = 1

        self.child_configs = self._get_child_configs()

    def _get_value(self):
        if self.config_type != CameraConfigType.SECTION:
            return self._config.get_value()
        else:
            return None

    def _get_child_configs(self):
        if self.config_type != CameraConfigType.SECTION:
            return None

        if self._config.count_children() < 1:
            return None

        return [CameraConfig(child, self._gp_sync) for child in self._config.get_children()]

    def _get_choices(self):
        if not self.config_type == CameraConfigType.RADIO and not self.config_type == CameraConfigType.MENU:
            return None

        choices = []
        for choice in self._config.get_choices():
            if not choice:
                continue

            choices.append(str(choice))
        return choices


class CameraConfigType(Enum):
    SECTION = gp.GP_WIDGET_SECTION
    TEXT = gp.GP_WIDGET_TEXT
    RANGE = gp.GP_WIDGET_RANGE
    TOGGLE = gp.GP_WIDGET_TOGGLE
    RADIO = gp.GP_WIDGET_RADIO
    MENU = gp.GP_WIDGET_MENU
    DATE = gp.GP_WIDGET_DATE
