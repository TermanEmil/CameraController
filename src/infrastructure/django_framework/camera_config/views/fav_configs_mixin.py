from adapters.camera.configs.camera_config_service import CameraConfigService
from camera_config.forms import ConfigFormSection
from camera_config.views.post_config_field_mixin import PostConfigFieldMixin


class FavConfigsMixin(PostConfigFieldMixin):
    camera_config_service: CameraConfigService = None

    def fav_configs_dispatch(self, request, camera_id: str):
        fav_configs = self.camera_config_service.get_favourite_configs(camera_id=camera_id)
        fav_configs_section = ConfigFormSection(name='favourite', label='Favourite', post_data=request.POST or None)
        fav_configs_section.add_fields(fields=fav_configs)

        if request.method == 'POST':
            for field in fav_configs_section.form_fields:
                self.post_config_field(camera_id=camera_id, config_field=field)

        return fav_configs_section