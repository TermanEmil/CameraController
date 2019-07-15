from django.shortcuts import render

from factories import CameraManagerFactory
from .object_not_found import camera_not_found


def live_preview(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    context = {
        'camera_name': camera.name,
        'camera_id': camera_id,
    }

    return render(request, 'camera_control/live_preview.html', context)
