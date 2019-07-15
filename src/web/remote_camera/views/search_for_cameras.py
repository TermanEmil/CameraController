from business.camera_manager import CameraManager
from django.http import HttpResponseRedirect


def search_for_cameras(request):
    camera_manager = CameraManager.instance()
    camera_manager.disconnect_all_cameras()
    camera_manager.find_all_cameras()

    # Redirect to previous page or smth.
    return HttpResponseRedirect(request.POST.get('next', '/'))
