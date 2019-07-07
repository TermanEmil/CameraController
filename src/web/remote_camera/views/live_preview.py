from business.CameraManager import CameraManager
from django.shortcuts import render

from .camera_not_found import camera_not_found
from ..forms import PreviewForm
from ..ids import *


def live_preview(request, camera_port):
    _parse_preview_form_post(request)

    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(camera_port)

    context = {
        'camera_port': camera_port,
        'form': _load_preview_form(request)
    }

    return render(request, 'remote_camera/live_preview.html', context)


def multi_live_preview(request):
    _parse_preview_form_post(request)

    context = {
        'camera_ports': [camera.port for camera in CameraManager.instance().cameras],
        'form': _load_preview_form(request)
    }

    return render(request, 'remote_camera/multi_live_preview.html', context)


def _parse_preview_form_post(request):
    if request.method != 'POST':
        return

    form = PreviewForm(request.POST)
    if not form.is_valid():
        return

    request.session[c_preview_quality_id] = form.get_preview_quality()


def _load_preview_form(request):
    return PreviewForm(initial={c_preview_quality_id: request.session.get(c_preview_quality_id, 1)})
