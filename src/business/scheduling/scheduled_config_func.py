from typing import Callable

from business.messaging.event_manager import EventManager
from business.scheduling.scheduled_config_repository import ScheduledConfigRepository
from enterprise.camera_ctrl.camera_manager import CameraManager


def scheduled_config_func(
        scheduled_config_id: int,
        scheduled_config_repository: ScheduledConfigRepository,
        camera_manager_provider: Callable[[], CameraManager],
        event_manager_provider: Callable[[], EventManager]):

    camera_manager = camera_manager_provider()
    event_manager = event_manager_provider()

    scheduled_config = scheduled_config_repository.get(scheduled_config_id)
    print('yohohoh')
    if scheduled_config is None:
        return

    cameras = camera_manager.cameras
    for camera in cameras:
        for config_to_change in scheduled_config.configs:
            # Exception handling?
            config = camera.get_single_config(config_name=config_to_change.name)

            if config is None:
                # Event, log? Skipping for now
                continue

            config.set_value(value=config_to_change.value)
            # Check if value changed. Log the result