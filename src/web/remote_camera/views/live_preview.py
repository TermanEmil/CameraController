from business.CameraManager import CameraManager
from django.shortcuts import render

from .camera_not_found import camera_not_found
from ..forms import PreviewForm
from ..ids import *
from ..utils.settings_manager import SettingsManager


def live_preview(request, camera_port):
    _parse_preview_form_post(request, camera_port)

    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    context = {
        'camera_port': camera.port,
        'form': _load_preview_form(request, camera)
    }

    return render(request, 'remote_camera/live_preview.html', context)


def multi_live_preview(request):
    context = {
        'camera_ports': [camera.port for camera in CameraManager.instance().cameras],
    }

    return render(request, 'remote_camera/multi_live_preview.html', context)


def _parse_preview_form_post(request, camera_port):
    if request.method != 'POST':
        return

    form = PreviewForm(request.POST)
    if not form.is_valid():
        return

    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return

    settings_manager = SettingsManager(request.session)
    camera_settings = settings_manager.get_settings(camera)

    camera_settings.quality = form.get_preview_quality()
    settings_manager.set_settings(camera, camera_settings)


def _load_preview_form(request, camera):
    settings_manager = SettingsManager(request.session)
    camera_settings = settings_manager.get_settings(camera)
    return PreviewForm(initial={c_preview_quality_id: camera_settings.quality})
