from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from django.shortcuts import render

from .camera_not_found import camera_not_found
from .view_models import CameraConfigSectionViewModel


def camera_config(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    assert isinstance(camera, CameraWrapper)

    configs = camera.get_config()
    context = {
        'config_sections': [CameraConfigSectionViewModel(config) for config in configs]
    }

    return render(request, 'remote_camera/camera_config.html', context)
