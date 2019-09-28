from django.views.generic import TemplateView

from adapters.camera.configs.camera_config_service import CameraConfigService
from business.camera.exceptions import CameraNotFoundException, CameraException
from shared.mixins.error_utils_mixin import ErrorUtilsMixin


class ConfigList(TemplateView, ErrorUtilsMixin):
    template_name = 'camera_config/config_list.html'
    camera_config_service: CameraConfigService = None

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        camera_id = kwargs['camera_id']
        context['camera_id'] = camera_id

        try:
            config_names = self.camera_config_service.get_all_config_names(camera_id=camera_id)
            context['config_names'] = list(config_names)

        except CameraException as e:
            return self.render_to_error(request=request, error=str(e))

        return self.render_to_response(context=context)