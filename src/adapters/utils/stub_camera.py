from enterprise.camera_ctrl.stub.stub_camera import StubCamera
from enterprise.camera_ctrl.stub.stub_camera_config import *
from enterprise.camera_ctrl.stub.stub_camera_manager import StubCameraManager


def create_stub_camera():
    cameras = [
        StubCamera(
            name='Nikon 6',
            camera_id='0',
            serial_nb='000',
            summary='Port: usb:000,020',
            config=_create_stub_config(),
        ),

        StubCamera(
            name='Nikon 6',
            camera_id='1',
            serial_nb='001',
            summary='Port: usb:000,022',
            config=_create_stub_config(),
        ),

        StubCamera(
            name='Nikon 6x0.2 Unicornslayer corporation M042.42_mpMk3',
            camera_id='2',
            serial_nb='002',
            summary='Port: usb:000,022',
            config=_create_stub_config(),
        ),

        StubCamera(
            name='Nikon 6',
            camera_id='3',
            serial_nb='003',
            summary='Port: usb:000,022',
            config=_create_stub_config(),
        ),
    ]

    return StubCameraManager(cameras=cameras)


def _create_stub_config():
    sections = {
        'actions': StubCameraConfigSection('actions', 'Actions', False, fields={
            'bulb': StubCameraConfigToggleField('bulb', 'Bulb', False, False, changes=False),
            'autofocusdrive': StubCameraConfigToggleField('autofocusdrive', 'Autofocusdrive', False, 1, changes=False),
            'autofocus': StubCameraConfigToggleField('autofocus', 'Autofocus', False, 1),
            'meow': StubCameraConfigTextField('meow', 'Meow', True, 'Meow'),
            'meow2': StubCameraConfigTextField('meow2', 'Meow 2', False, 'Meow'),
            'meow3': StubCameraConfigTextField('meow3', 'Meow 3', False, 'Meow', changes=False),
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