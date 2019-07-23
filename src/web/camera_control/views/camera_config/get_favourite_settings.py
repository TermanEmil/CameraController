from camera_control.models import FavField
from factories import CameraManagerFactory, FavConfigsManagerFactory
from forms import CameraSingleConfigForm
from views.object_not_found import camera_not_found


def get_favourite_settings(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    fav_configs_manager = FavConfigsManagerFactory.get()
    profile = fav_configs_manager.get_profile(request)

    config_forms = []
    for field in profile.fields.all:
        assert isinstance(field, FavField)

        config = camera.get_single_config(field.name)
        if config is None:
            continue

        form = CameraSingleConfigForm(config)
        config_forms.append(form)