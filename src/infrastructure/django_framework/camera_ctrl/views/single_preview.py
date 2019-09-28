from django.views.generic import TemplateView

from adapters.camera.configs.camera_config_service import CameraConfigService
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException
from camera_config.views.fav_configs_mixin import FavConfigsMixin
from shared.mixins.error_utils_mixin import ErrorUtilsMixin
from ._utils import map_camera_to_view_model


class SinglePreview(TemplateView, FavConfigsMixin, ErrorUtilsMixin):
    template_name = 'camera_ctrl/single_preview.html'

    camera_ctrl_service: CameraCtrlService = None
    camera_config_service: CameraConfigService = None

    def dispatch(self, request, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        camera_id = kwargs['camera_id']

        try:
            camera = self.camera_ctrl_service.camera_get(camera_id=camera_id)

            context['camera'] = map_camera_to_view_model(camera)
            context['form'] = self.fav_configs_dispatch(request=request, camera_id=camera_id)

        except CameraException as e:
            return self.render_to_error(request=request, error=str(e))

        return self.render_to_response(context=context)
