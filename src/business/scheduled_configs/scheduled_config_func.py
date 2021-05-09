from typing import Callable

from business.messaging.event_manager import EventManager
from business.scheduled_configs.events import ScheduledConfigEvents
from business.scheduled_configs.scheduled_config_repository import ScheduledConfigRepository
from enterprise.camera_ctrl.camera_manager import CameraManager


def scheduled_config_func(
        scheduled_config_id: int,
        scheduled_config_repository: ScheduledConfigRepository,
        camera_manager_provider: Callable[[], CameraManager],
        event_manager_provider: Callable[[], EventManager]):

    camera_manager = camera_manager_provider()
    event_manager = event_manager_provider()

    scheduled_config = scheduled_config_repository.get(scheduled_config_id)
    if scheduled_config is None:
        return

    for camera in camera_manager.cameras:
        for config_to_change in scheduled_config.configs:
            # Try get config
            try:
                config = camera.get_single_config(config_name=config_to_change.name)
            except Exception as e:
                event_manager.trigger_event(
                    ScheduledConfigEvents.CONFIG_GET_ERROR,
                    kwargs={'config_field': config_to_change, 'camera': camera, 'exception': e})
                continue

            if config is None:
                event_manager.trigger_event(
                    ScheduledConfigEvents.CONFIG_MISSING,
                    kwargs={'config_field': config_to_change, 'camera': camera})
                continue

            initial_config_value = config.value

            # Set config value
            try:
                config.set_value(value=config_to_change.value)
                camera.set_config((config,))
            except Exception as e:
                event_manager.trigger_event(
                    ScheduledConfigEvents.CONFIG_SET_ERROR,
                    kwargs={'config_field': config_to_change, 'camera': camera, 'exception': e})
                continue

            # Verify config changed
            try:
                config = camera.get_single_config(config_name=config_to_change.name)
            except Exception as e:
                event_manager.trigger_event(
                    ScheduledConfigEvents.CONFIG_GET_ERROR,
                    kwargs={'config_field': config_to_change, 'camera': camera, 'exception': e})
                continue

            if str(config.value) != config_to_change.value:
                event_manager.trigger_event(
                    ScheduledConfigEvents.CONFIG_FAILED_TO_CHANGE_ERROR,
                    kwargs={'config_field': config_to_change, 'camera': camera, 'current_config_value': config.value})
                continue

            # Success
            event_manager.trigger_event(
                ScheduledConfigEvents.CONFIG_SET,
                kwargs={'config_field': config_to_change, 'camera': camera, 'initial_config_value': str(initial_config_value)})
