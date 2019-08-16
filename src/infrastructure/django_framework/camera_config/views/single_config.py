from django.views.generic import TemplateView

from adapters.camera.configs.camera_config_service import CameraConfigService
from camera_config.forms import SingleConfigForm
from camera_config.views.post_config_field_mixin import PostConfigFieldMixin
from shared.mixins.error_utils_mixin import ErrorUtilsMixin


class SingleConfig(TemplateView, PostConfigFieldMixin, ErrorUtilsMixin):
    template_name = 'camera_config/single_config.html'
    camera_config_service: CameraConfigService = None

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        camera_id = kwargs['camera_id']
        context['camera_id'] = camera_id

        config_name = kwargs['config_name']

        try:
            config = self.camera_config_service.get_config(camera_id=camera_id, config_name=config_name)
            form = SingleConfigForm.from_config_dto(config_dto=config, post_data=request.POST or None)
            context['form'] = form

            if request.method == 'POST':
                self.post_config_field(camera_id=camera_id, config_field=form)

        except Exception as e:
            return self.render_to_error(request=request, error=str(e))

        return self.render_to_response(context=context)