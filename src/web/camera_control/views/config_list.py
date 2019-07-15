from django.shortcuts import render

from factories import CameraManagerFactory
from .object_not_found import camera_not_found


def config_list(request, camera_id):
    camera_manager = CameraManagerFactory.get()
    camera = camera_manager.get_camera(camera_id)

    if camera is None:
        return camera_not_found(request, camera_id)

    context = {
        'config_names': camera.list_configs(),
        'camera_name': camera.name,
        'camera_id': camera_id
    }

    return render(request, 'camera_control/config_list.html', context)
