from django.views.generic import TemplateView

from adapters.camera.configs.camera_config_service import CameraConfigService
from business.camera.exceptions import CameraException
from camera_config.views.post_config_field_mixin import PostConfigFieldMixin
from shared.mixins.error_utils_mixin import ErrorUtilsMixin
from ..forms import CameraConfigFormManager


class AllConfigs(TemplateView, PostConfigFieldMixin, ErrorUtilsMixin):
    template_name = 'camera_config/all_configs.html'
    camera_config_service: CameraConfigService = None

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        camera_id = kwargs['camera_id']
        context['camera_id'] = camera_id

        try:
            configs_dto = self.camera_config_service.get_all_configs(camera_id=camera_id)

            config_form_manager = CameraConfigFormManager(request.POST or None)
            config_form_manager.load_from_configs_dto(configs=configs_dto)

            if request.method == 'POST':
                self.post(camera_id=camera_id, config_form_manager=config_form_manager)

        except CameraException as e:
            return self.render_to_error(request=request, error=str(e))

        context['form'] = config_form_manager
        return self.render_to_response(context=context)

    def post(self, camera_id: str, config_form_manager: CameraConfigFormManager):
        for section in config_form_manager.sections:
            for field in section.form_fields:
                self.post_config_field(camera_id=camera_id, config_field=field)