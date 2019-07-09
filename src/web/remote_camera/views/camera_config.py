from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from django.shortcuts import render
from ..forms import CameraConfigForm

from .camera_not_found import camera_not_found
from .view_models import CameraConfigViewModel


def camera_config(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    assert isinstance(camera, CameraWrapper)

    config_view_model = CameraConfigViewModel(camera.get_config())
    config_form = CameraConfigForm(config_view_model.form_fields)

    fields_dict = {}
    for field in config_form.visible_fields():
        fields_dict[field.name] = field

    context = {
        'camera_port': camera_port,
        'config': config_view_model,
        'form': config_form,
        'fields_dict': fields_dict
    }

    return render(request, 'remote_camera/camera_config.html', context)
