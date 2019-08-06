from business.camera_control.stub.stub_camera import StubCamera
from business.camera_control.stub.stub_camera_manager import StubCameraManager
from business.camera_control.stub.stub_camera_config import *
from business.camera_control.gphoto2.gp_camera_manager import GpCameraManager
from business.camera_control.camera_manager import CameraManager
from utils.fav_configs_manager import FavConfigsManager

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import BaseScheduler


class CameraManagerFactory:
    _instance = None

    @staticmethod
    def get() -> CameraManager:
        if CameraManagerFactory._instance is None:
            # CameraManagerFactory._instance = CameraManagerFactory._create_stub()
            CameraManagerFactory._instance = GpCameraManager()

        return CameraManagerFactory._instance

    @staticmethod
    def _create_stub():
        cameras = [
            StubCamera(
                name='Nikon 6',
                camera_id='0',
                serial_nb='000',
                summary='Port: usb:000,020',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='1',
                serial_nb='001',
                summary='Port: usb:000,022',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='2',
                serial_nb='002',
                summary='Port: usb:000,022',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='3',
                serial_nb='003',
                summary='Port: usb:000,022',
                config=CameraManagerFactory._create_stub_config(),
            ),
        ]

        return StubCameraManager(cameras=cameras)

    @staticmethod
    def _create_stub_config():
        sections = {
            'actions': StubCameraConfigSection('actions', 'Actions', False, fields={
                'bulb': StubCameraConfigToggleField('bulb', 'Bulb', False, 0),
                'meow': StubCameraConfigTextField('meow', 'Meow', True, 'Meow'),
                'meow2': StubCameraConfigTextField('meow2', 'Meow 2', False, 'Meow'),
            }),

            'capture': StubCameraConfigSection('capture', 'Capture', False, fields={
                'quality': StubCameraConfigChoiceField(
                    'quality',
                    'Quality',
                    False, 'Best',
                    choices=['Bad', 'Good', 'Best']),

                'shuterspeed': StubCameraConfigRangeField(
                    'shuterspeed',
                    'Shuterspeed',
                    is_readonly=False,
                    value=0.5,
                    range_min=0.0,
                    range_max=1.0),

                'shuterspeed2': StubCameraConfigRangeField(
                    'shuterspeed2',
                    'Shuterspeed2',
                    is_readonly=False,
                    value=0.5,
                    range_min=0.0,
                    range_max=1.0),

                'shuterspeed3': StubCameraConfigRangeField(
                    'shuterspeed3',
                    'Shuterspeed3',
                    is_readonly=False,
                    value=0.5,
                    range_min=0.0,
                    range_max=1.0),

                'shuterspeed4': StubCameraConfigRangeField(
                    'shuterspeed4',
                    'Shuterspeed4',
                    is_readonly=False,
                    value=0.5,
                    range_min=0.0,
                    range_max=1.0),

                'shuterspeed5': StubCameraConfigRangeField(
                    'shuterspeed5',
                    'Shuterspeed5',
                    is_readonly=False,
                    value=0.5,
                    range_min=0.0,
                    range_max=1.0),

                'date': StubCameraConfigField('date', 'Date', False, '12314232T131')
            }),
        }
        return StubCameraConfig(sections)


class FavConfigsManagerFactory:
    @staticmethod
    def get():
        return FavConfigsManager()


class ApSchedulerFactory:
    _instance = None

    @staticmethod
    def get() -> BaseScheduler:
        if ApSchedulerFactory._instance is None:
            ApSchedulerFactory._instance = BackgroundScheduler()

        return ApSchedulerFactory._instance