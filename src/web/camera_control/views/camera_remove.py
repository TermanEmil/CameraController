from django.http import JsonResponse

from factories import CameraManagerFactory
from .object_not_found import camera_not_found


def camera_remove(request, camera_id):
    camera_manager = CameraManagerFactory.get()
    camera = camera_manager.get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    camera_manager.remove_camera(camera_id)
    return JsonResponse({})
