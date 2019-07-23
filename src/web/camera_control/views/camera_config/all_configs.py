from django.shortcuts import render

from business.camera_control.camera import Camera
from business.camera_control.camera_config import CameraConfig, CameraConfigField
from factories import CameraManagerFactory, FavConfigsManagerFactory
from views.object_not_found import camera_not_found
from forms import CameraConfigForm


def all_configs(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    config = camera.get_config()
    form = _build_form(request, camera, config)

    if request.method == 'POST':
        _process_post_request(camera, form, config)

    context = {
        'camera_name': camera.name,
        'camera_id': camera_id,
        'form': form,
    }

    return render(request, 'camera_control/camera_config/all_configs.html', context)


def _build_form(request, camera: Camera, config: CameraConfig):
    form = CameraConfigForm(request.POST or None)

    fav_configs = FavConfigsManagerFactory.get().extract_configs(request, camera)
    form.add_fields(fav_configs, section_label='Favourites', section_name='favourites')
    
    form.load_from_camera_config(config)

    return form


def _process_post_request(camera: Camera, form: CameraConfigForm, config: CameraConfig):
    if not form.is_valid():
        return

    changed_fields = []
    for field_name in form.changed_data:
        field = config.all_fields.get(field_name)

        if field is None:
            continue

        assert isinstance(field, CameraConfigField)

        try:
            config_changed = field.set_value(form.cleaned_data[field_name])
            if config_changed:
                changed_fields.append(field)
        except Exception as e:
            form.add_error(field_name, str(e))

    try:
        camera.set_config(changed_fields)
    except Exception as e:
        form.add_error(None, str(e))

    if len(form.errors) > 0:
        form.add_error(None, 'There are errors')