import time

from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper, CameraConfig
from django.shortcuts import render
import logging
from .camera_not_found import camera_not_found
from ..forms import CameraConfigForm


def camera_config(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    assert isinstance(camera, CameraWrapper)

    config = camera.get_config()
    config_form = CameraConfigForm(config, request.POST or None)

    if request.method == 'POST':
        config_form = CameraConfigForm(config, request.POST)
        if not config_form.is_valid():
            logging.warning('Form contains errors')
        else:
            # try:
            config.set_values(config_form.cleaned_data)
            camera.set_config(config)
            # except Exception as e:
            #     config_form.add_error(None, str(e))

    context = {
        'camera_port': camera_port,
        'form': config_form,
    }

    return render(request, 'remote_camera/camera_config.html', context)
