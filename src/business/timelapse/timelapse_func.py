import os
import sys
import threading
from datetime import datetime
from typing import Callable

import pytz

from business.scheduling.timelapse_repository import TimelapseRepository
from business.timelapse.naming_tricks import apply_naming_tricks
from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager


def timelapse_func(
        timelapse_id: int,
        timelapse_repository: TimelapseRepository,
        camera_manager_provider: Callable[[], CameraManager]):

    timelapse = timelapse_repository.get(pk=timelapse_id)

    now = datetime.now(tz=pytz.utc)
    img_capture_tasks = []

    camera_manager = camera_manager_provider()
    for camera in camera_manager.cameras:
        storage_dir = apply_naming_tricks(
            name_format=timelapse.storage_dir_format,
            time=now,
            timelapse=timelapse,
            camera=camera
        )

        filename = apply_naming_tricks(
            name_format=timelapse.filename_format,
            time=now,
            timelapse=timelapse,
            camera=camera
        )

        try:
            if not os.path.isdir(storage_dir):
                os.makedirs(storage_dir, exist_ok=True)
        except Exception as e:
            print('Failed to create directory {}: {}'.format(storage_dir, e), file=sys.stderr)
            continue

        img_capture_tasks.append(threading.Thread(target=_capture_picture, args=(camera, storage_dir, filename,)))

    for capture_task in img_capture_tasks:
        capture_task.start()

    for capture_task in img_capture_tasks:
        capture_task.join()

    timelapse.capture_index += 1
    timelapse_repository.update(timelapse)
    print('---------------------', timelapse.capture_index)


def _capture_picture(camera: Camera, storage_dir: dir, filename: dir):
    camera.capture_img(storage_dir, filename)
    print('Captured photo with ', camera.name)