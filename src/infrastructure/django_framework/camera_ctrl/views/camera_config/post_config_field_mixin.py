from adapters.camera.configs.camera_config_service import CameraConfigService
from business.camera.exceptions import CameraException
from camera_ctrl.views.camera_config._forms import SingleConfigForm
from shared.di import obj_graph


class PostConfigFieldMixin:
    camera_config_service = obj_graph().provide(CameraConfigService)

    def post_config_field(self, camera_id: str, config_field: SingleConfigForm):
        form = config_field

        if len(form.visible_fields()) == 0 or form.field.disabled:
            return

        if not (form.is_valid() and form.has_changed()):
            return

        try:
            self.camera_config_service.set_config(
                camera_id=camera_id,
                config_name=form.name,
                config_value=form.cleaned_data.get(form.name))

            form.tried_to_change = True

            # Check if it actually changed
            field_config = self.camera_config_service.get_config(camera_id=camera_id, config_name=form.name)
            form.managed_to_change = (field_config.value == form.cleaned_data[form.name])

            # Set the current value if it didn't change
            if not form.managed_to_change:
                form.set_value(field_config.value)

        except CameraException as e:
            form.add_error(form.name, str(e))