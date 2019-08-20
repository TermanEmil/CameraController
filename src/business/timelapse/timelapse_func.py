import os
import sys
import threading
from datetime import datetime
from typing import Callable, Iterable

from business.messaging.event_manager import EventManager
from business.scheduling.timelapse_repository import TimelapseRepository
from business.timelapse.events import TimelapseEvents
from business.timelapse.naming_tricks import apply_naming_tricks
from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager
from enterprise.scheduling.timelapse import Timelapse


def timelapse_func(
        timelapse_id: int,
        timelapse_repository: TimelapseRepository,
        camera_manager_provider: Callable[[], CameraManager],
        event_manager_provider: Callable[[], EventManager]):

    event_manager = event_manager_provider()

    timelapse = timelapse_repository.get(pk=timelapse_id)
    img_capture_tasks = list(_create_img_capture_tasks(
        cameras=camera_manager_provider().cameras,
        now=datetime.utcnow(),
        timelapse=timelapse,
        event_manager=event_manager))

    for capture_task in img_capture_tasks:
        capture_task.start()

    for capture_task in img_capture_tasks:
        capture_task.join()

    timelapse.capture_index += 1
    timelapse_repository.update(timelapse)

    event_manager.trigger_event(TimelapseEvents.ALL_PHOTOS_TAKEN, kwargs={'timelapse': timelapse})


def _create_img_capture_tasks(
        cameras: Iterable[Camera],
        now: datetime,
        timelapse: Timelapse,
        event_manager: EventManager):

    for camera in cameras:
        storage_dir = apply_naming_tricks(
            name_format=timelapse.storage_dir_format,
            time=now,
            timelapse=timelapse,
            camera=camera)

        filename = apply_naming_tricks(
            name_format=timelapse.filename_format,
            time=now,
            timelapse=timelapse,
            camera=camera)

        try:
            if not os.path.isdir(storage_dir):
                os.makedirs(storage_dir, exist_ok=True)
        except Exception as e:
            error = 'Failed to create directory {}: {}'.format(storage_dir, e)
            event_manager.trigger_event(TimelapseEvents.CAPTURE_ERROR, kwargs={'camera': camera, 'error': error})
            continue

        yield threading.Thread(target=_capture_picture, args=(camera, storage_dir, filename, event_manager))


def _capture_picture(camera: Camera, storage_dir: dir, filename: dir, event_manager: EventManager):
    try:
        filepath = camera.capture_img(storage_dir, filename)
    except Exception as e:
        event_manager.trigger_event(TimelapseEvents.CAPTURE_ERROR, kwargs={'camera': camera, 'error': str(e)})
        return

    event_manager.trigger_event(TimelapseEvents.PHOTO_TAKEN, kwargs={'camera': camera, 'filepath': filepath})