from typing import Callable

from business.messaging.event_manager import EventManager
from business.timelapse.timelapse_repository import TimelapseRepository
from business.timelapse.timelapse_func import timelapse_func
from enterprise.camera_ctrl.camera_manager import CameraManager


class GetTimelapseFuncBlRule:
    class Dto:
        def __init__(self, func: Callable, kwags: dict):
            self.func = func
            self.kwargs = kwags

    def __init__(
            self,
            timelapse_repository: TimelapseRepository,
            camera_manager_provider: Callable[[], CameraManager],
            event_manager_provider: Callable[[], EventManager]):

        self._timelapse_repository = timelapse_repository
        self._camera_manager_provider = camera_manager_provider
        self._event_manager_provider = event_manager_provider

    def execute(self, timelapse_id: int) -> 'GetTimelapseFuncBlRule.Dto':
        kwags = {
            'timelapse_id': timelapse_id,
            'timelapse_repository': self._timelapse_repository,
            'camera_manager_provider': self._camera_manager_provider,
            'event_manager_provider': self._event_manager_provider}

        return self.Dto(func=timelapse_func, kwags=kwags)