from typing import Optional

import pinject
from apscheduler.schedulers.background import BackgroundScheduler
from pinject.object_graph import ObjectGraph

from adapters.utils.stub_camera import create_stub_camera
from business.messaging.event_manager import EventManager
from enterprise.camera_ctrl.camera_manager import CameraManager
from enterprise.camera_ctrl.gphoto2.gp_camera_manager import GpCameraManager
from scheduling.implementations.aps_scheduler import ApsScheduler
from shared.repositories.timelapse_repository import TimelapseRepository
from .repositories.favourite_config_repository import FavouriteConfigRepository
from .repositories.cron_schedule_repository import CronScheduleRepository

# Imports used by pinject
from .di_imports import pinject_imports


class CameraManagerSingleton:
    instance: CameraManager = None

    @staticmethod
    def get() -> CameraManager:
        if CameraManagerSingleton.instance is None:
            # CameraManagerSingleton.instance = create_stub_camera()
            CameraManagerSingleton.instance = GpCameraManager()

        return CameraManagerSingleton.instance


class EventManagerSingleton:
    instance: EventManager = None

    @staticmethod
    def get() -> EventManager:
        if EventManagerSingleton.instance is None:
            EventManagerSingleton.instance = EventManager()

        return EventManagerSingleton.instance


class DjangoProjectBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('camera_manager_provider', to_instance=CameraManagerSingleton.get)
        bind('camera_manager', to_instance=CameraManagerSingleton.get())

        bind('favourite_config_repository', to_class=FavouriteConfigRepository)
        bind('cron_schedule_repository', to_class=CronScheduleRepository)
        bind('timelapse_repository', to_class=TimelapseRepository)

        bind('scheduler', to_class=ApsScheduler)
        bind('aps_scheduler', to_class=BackgroundScheduler)

        bind('event_manager_provider', to_instance=EventManagerSingleton.get)
        bind('event_manager', to_instance=EventManagerSingleton.get())


_obj_graph: Optional[ObjectGraph] = None


def obj_graph() -> ObjectGraph:
    global _obj_graph

    if _obj_graph is None:
        pinject_imports()
        _obj_graph = pinject.new_object_graph(binding_specs=(DjangoProjectBindingSpec(),))

    return _obj_graph

