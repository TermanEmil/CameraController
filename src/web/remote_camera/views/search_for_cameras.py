from business.CameraManager import CameraManager
from django.http import HttpResponseRedirect


def search_for_cameras(request):
    camera_manager = CameraManager.instance()
    camera_manager.disconnect_all_cameras()
    camera_manager.autodetect_all_cameras()

    return HttpResponseRedirect(request.POST.get('next', '/'))
