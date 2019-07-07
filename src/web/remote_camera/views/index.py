from business.CameraManager import CameraManager
from django.shortcuts import render
from .view_models import CameraViewModel


def index(request):
    camera_manager = CameraManager.instance()
    camera_manager.disconnect_all_cameras()
    camera_manager.autodetect_all_cameras()

    context = {
        'cameras': [CameraViewModel(camera) for camera in camera_manager.cameras]
    }

    return render(request, 'remote_camera/index.html', context)
