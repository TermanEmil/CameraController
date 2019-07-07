from business.CameraManager import CameraManager
from django.shortcuts import render

from .camera_not_found import camera_not_found
from ..forms import PreviewForm
from ..ids import *


def live_preview(request, camera_port):
    if request.method == 'POST':
        form = PreviewForm(request.POST)
        if form.is_valid():
            request.session[c_preview_quality_id] = form.get_preview_quality()

    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(camera_port)

    context = {
        'camera_port': camera_port,
        'form': _load_preview_form(request)
    }

    return render(request, 'remote_camera/live_preview.html', context)


def _load_preview_form(request):
    return PreviewForm(initial={c_preview_quality_id: request.session.get(c_preview_quality_id, 1)})
