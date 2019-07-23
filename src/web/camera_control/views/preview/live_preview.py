from django.shortcuts import render

from factories import CameraManagerFactory, FavConfigsManagerFactory
from forms import CameraSingleConfigForm
from views.object_not_found import camera_not_found


def live_preview(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    field_forms = list(_manage_favourite_configs(request, camera))

    context = {
        'camera_name': camera.name,
        'camera_id': camera_id,
        'field_forms': field_forms
    }

    return render(request, 'camera_control/preview/live_preview.html', context)


def _manage_favourite_configs(request, camera):
    fav_configs = FavConfigsManagerFactory.get().extract_configs(request, camera)

    for config in fav_configs:
        form = CameraSingleConfigForm(config, request.POST or None)
        if len(form.visible_fields()) == 0:
            continue

        if request.method == 'POST' and form.is_valid():
            if form.has_changed():
                try:
                    config.set_value(form.cleaned_data[config.name])
                    camera.set_config([config])

                    config = camera.get_single_config(config.name)
                    form = CameraSingleConfigForm(config)
                except Exception as e:
                    form.add_error(config.name, str(e))

        yield form
