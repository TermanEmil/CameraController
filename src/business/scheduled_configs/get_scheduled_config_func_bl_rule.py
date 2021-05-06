from typing import Callable

from business.messaging.event_manager import EventManager
from business.scheduled_configs.scheduled_config_func import scheduled_config_func
from business.scheduled_configs.scheduled_config_repository import ScheduledConfigRepository
from enterprise.camera_ctrl.camera_manager import CameraManager


class GetScheduledConfigFuncBlRule:
    class Dto:
        def __init__(self, func: Callable, kwags: dict):
            self.func = func
            self.kwargs = kwags

    def __init__(
            self,
            scheduled_config_repository: ScheduledConfigRepository,
            camera_manager_provider: Callable[[], CameraManager],
            event_manager_provider: Callable[[], EventManager]):

        self._scheduled_config_repository = scheduled_config_repository
        self._camera_manager_provider = camera_manager_provider
        self._event_manager_provider = event_manager_provider

    def execute(self, scheduled_config_id: int) -> 'GetScheduledConfigFuncBlRule.Dto':
        kwags = {
            'scheduled_config_id': scheduled_config_id,
            'scheduled_config_repository': self._scheduled_config_repository,
            'camera_manager_provider': self._camera_manager_provider,
            'event_manager_provider': self._event_manager_provider}

        return self.Dto(func=scheduled_config_func, kwags=kwags)
