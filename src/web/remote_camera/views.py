from django.shortcuts import render
from CameraManager import CameraManager
from CameraWrapper import CameraWrapper
from . import view_models
import gphoto2 as gp


def index(request):
    camera_manager = CameraManager.instance()
    camera_manager.autodetect_all_cameras()

    camera_manager.cameras = [
        CameraWrapper(gp.Camera(), camera_name='Nikon 6_2', port='usb00:020'),
        CameraWrapper(gp.Camera(), camera_name='Nikon 6_3', port='usb00:040')
    ]

    context = {
        'cameras': [view_models.CameraViewModel(camera) for camera in camera_manager.cameras]
    }
    return render(request, 'remote_camera/index.html', context)

