from django.http import HttpResponseRedirect
from factories import CameraManagerFactory


def camera_search(request):
    camera_manager = CameraManagerFactory.get()
    camera_manager.detect_all_cameras()

    # Redirect to previous page or smth.
    return HttpResponseRedirect(request.POST.get('next', '/'))

