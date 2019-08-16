import pinject
from apscheduler.schedulers.background import BackgroundScheduler

from adapters.utils.stub_camera import create_stub_camera
from enterprise.camera_ctrl.camera_manager import CameraManager
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
            CameraManagerSingleton.instance = create_stub_camera()
            # CameraManagerSingleton.instance = GpCameraManager()

        return CameraManagerSingleton.instance


class DjangoProjectBindingSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind('camera_manager', to_instance=CameraManagerSingleton.get())

        bind('favourite_config_repository', to_class=FavouriteConfigRepository)
        bind('cron_schedule_repository', to_class=CronScheduleRepository)
        bind('timelapse_repository', to_class=TimelapseRepository)

        bind('scheduler', to_class=ApsScheduler)
        bind('aps_scheduler', to_class=BackgroundScheduler)

        bind('camera_manager_provider', to_instance=CameraManagerSingleton.get)


pinject_imports()
obj_graph = pinject.new_object_graph(
    binding_specs=(DjangoProjectBindingSpec(),))