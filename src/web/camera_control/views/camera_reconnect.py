from django.http import JsonResponse

from factories import CameraManagerFactory
from .object_not_found import camera_not_found


def camera_reconnect(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    camera.disconnect()
    return JsonResponse({})