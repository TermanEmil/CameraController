from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from django.shortcuts import render
from .view_models import CameraViewModel, CameraConfigSection


from .camera_not_found import camera_not_found


def camera_config(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    assert isinstance(camera, CameraWrapper)

    configs = camera.get_config()
    context = {
        'config_sections': [CameraConfigSection(config) for config in configs]
    }

    return render(request, 'remote_camera/camera_config.html', context)
