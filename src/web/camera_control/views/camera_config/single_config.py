from django.shortcuts import render

from business.camera_control.camera import Camera
from business.camera_control.camera_config import CameraConfigField
from factories import CameraManagerFactory
from views.object_not_found import camera_not_found, object_not_found
from forms import CameraSingleConfigForm


def single_config(request, camera_id, config_name):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    config_field = camera.get_single_config(config_name)
    if config_field is None:
        _config_not_found(request, camera, config_name)

    form = CameraSingleConfigForm(config_field, request.POST or None)
    if len(form.visible_fields()) == 0:
        return _cant_modify_field(request, config_field)

    if request.method == 'POST' and form.is_valid():
        try:
            config_field.set_value(form.cleaned_data[config_name])
            camera.set_config([config_field])

            config_field = camera.get_single_config(config_name)
            form = CameraSingleConfigForm(config_field)
        except Exception as e:
            form.add_error(config_name, str(e))

    context = {
        'camera_name': camera.name,
        'camera_id': camera_id,
        'config_name': config_field.name,
        'form': form,
    }

    return render(request, 'camera_control/camera_config/single_config.html', context)


def _config_not_found(request, camera: Camera, config_name):
    msg_format = 'Could not find a camera_config with id = {0} on camera with {1} with id = {2}'
    return object_not_found(request, msg_format.format(config_name, camera.name, camera.id))


def _cant_modify_field(request, config_field: CameraConfigField):
    msg_format = "{0}: currently, it's not supported to modify this field"
    return object_not_found(request, msg_format.format(config_field.name))
