import logging

from business.camera_wrapper import CameraWrapper
from django.shortcuts import render

from .camera_not_found import camera_not_found
from ..forms import CameraConfigForm
from ..factories import CameraManagerFactory


def camera_config(request, camera_port):
    camera = CameraManagerFactory.get().get_camera_on_port(camera_port)
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
            changed_data_dict = ((key, config_form.cleaned_data[key])for key in config_form.changed_data)
            camera.set_config(config, dict(changed_data_dict))

            # Reload the config, because not all the fields can change.
            config = camera.get_config()
            config_form = CameraConfigForm(config)

    context = {
        'camera_port': camera_port,
        'form': config_form
    }

    return render(request, 'remote_camera/camera_config.html', context)

