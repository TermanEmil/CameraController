import os
from typing import Optional, TypeVar

import pinject
from apscheduler.schedulers.background import BackgroundScheduler
from pinject.object_graph import ObjectGraph

from business.messaging.event_manager import EventManager
from enterprise.camera_ctrl.camera_manager import CameraManager
from infrastructure.camera_glue_code.gphoto2.gp_camera_manager import GpCameraManager
from infrastructure.camera_glue_code.stub.create_stub_cameras import create_stub_cameras
from proj_settings.settings_facade import SettingsFacade
from scheduling.implementations.aps_scheduler import ApsScheduler
from shared.implementations.django_email_sender import DjangoEmailSender
from shared.repositories.timelapse_repository import TimelapseRepository
from .di_imports import pinject_imports
from .repositories.cron_schedule_repository import CronScheduleRepository
from .repositories.favourite_config_repository import FavouriteConfigRepository


class CameraManagerSingleton:
    instance: CameraManager = None

    @staticmethod
    def get() -> CameraManager:
        if CameraManagerSingleton.instance is None:
            if 'USE_STUB' in os.environ:
                CameraManagerSingleton.instance = create_stub_cameras()
            else:
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

        bind('emailing_settings', to_class=SettingsFacade)
        bind('email_sender', to_class=DjangoEmailSender)


class ObjectGraphWrapper:
    """A wrapper to allow typing"""

    T = TypeVar('T')

    def __init__(self, pinject_obj_graph: ObjectGraph):
        self._obj_graph = pinject_obj_graph

    def provide(self, cls: T) -> T:
        return self._obj_graph.provide(cls)


_obj_graph: Optional[ObjectGraphWrapper] = None


def obj_graph() -> ObjectGraphWrapper:
    global _obj_graph

    if _obj_graph is None:
        pinject_imports()
        pinject_obj_graph = pinject.new_object_graph(binding_specs=(DjangoProjectBindingSpec(),))
        _obj_graph = ObjectGraphWrapper(pinject_obj_graph)

    return _obj_graph
