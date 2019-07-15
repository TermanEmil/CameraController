from django.shortcuts import render

from business.camera_control.camera_config import CameraConfigField
from factories import CameraManagerFactory
from views.object_not_found import camera_not_found
from forms import CameraConfigForm


def all_configs(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    config = camera.get_config()
    form = CameraConfigForm(config, request.POST or None)

    if request.method == 'POST' and form.is_valid():
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

        # Reload the configs, because not all fields can change.
        config = camera.get_config()
        errors = form.errors
        cleaned_data = form.cleaned_data
        form = CameraConfigForm(config)
        form.cleaned_data = cleaned_data
        for k, v in errors.items():
            form.add_error(k, v)

    context = {
        'camera_name': camera.name,
        'camera_id': camera_id,
        'form': form,
    }

    return render(request, 'camera_control/all_configs.html', context)