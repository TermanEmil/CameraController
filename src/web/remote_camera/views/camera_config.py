from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from django.shortcuts import render
from .view_models import CameraViewModel

from .camera_not_found import camera_not_found


def camera_config(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    assert isinstance(camera, CameraWrapper)

    config = camera.get_config()
    print(config)
    context = {
        'cameras': [CameraViewModel(camera) for camera in CameraManager.instance().cameras]
    }

    return render(request, 'remote_camera/index.html', context)
