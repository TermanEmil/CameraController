from datetime import datetime

from enterprise.camera_ctrl.camera import Camera
from enterprise.scheduling.timelapse import Timelapse


class LazyFormatDictIgnoreMissing(dict):
    def __getitem__(self, key):
        func = dict.__getitem__(self, key)

        if callable(func):
            return func()

        return super().__getitem__(key)

    def __missing__(self, key):
        return '{' + key + '}'


# Use lazy dictionary values because some of these values may be computing intensive and may not even be used.
def apply_naming_tricks(name_format, time: datetime, timelapse: Timelapse, camera: Camera):
    format_args = LazyFormatDictIgnoreMissing({
        'timestamp': lambda: time.timestamp() * 1000,
        'time': lambda: time,
        'capture_index': lambda: timelapse.capture_index,

        'camera_id': lambda: camera.id,
        'camera_serial_nb': lambda: camera.serial_nb,
        'camera_name': lambda: camera.name,

        'timelapse_name': lambda: timelapse.name,
        'timelapse_id': lambda: timelapse.pk
    })

    return name_format.format_map(format_args)