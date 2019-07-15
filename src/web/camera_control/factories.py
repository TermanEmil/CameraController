from business.camera_control.stub.stub_camera import StubCamera
from business.camera_control.stub.stub_camera_manager import StubCameraManager
from business.camera_control.stub.stub_camera_config import *
from business.camera_control.gphoto2.gp_camera_manager import GpCameraManager


class CameraManagerFactory:
    instance = None

    @staticmethod
    def get():
        if CameraManagerFactory.instance is None:
            # CameraManagerFactory.instance = CameraManagerFactory._create_stub()
            CameraManagerFactory.instance = GpCameraManager()

        return CameraManagerFactory.instance

    @staticmethod
    def _create_stub():
        cameras = [
            StubCamera(
                name='Nikon 6',
                camera_id='0',
                summary='Port: usb:000,020',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='1',
                summary='Port: usb:000,022',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='2',
                summary='Port: usb:000,022',
                config=CameraManagerFactory._create_stub_config(),
            ),

            StubCamera(
                name='Nikon 6',
                camera_id='3',
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

                'date': StubCameraConfigField('date', 'Date', False, '12314232T131')
            }),
        }
        return StubCameraConfig(sections)