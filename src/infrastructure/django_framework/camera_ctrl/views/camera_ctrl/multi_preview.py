from django.views.generic import TemplateView

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from shared.di import obj_graph
from ._utils import map_cameras_to_view_models


class MultiPreview(TemplateView):
    template_name = 'camera_ctrl/multi_preview.html'

    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cameras = self.camera_ctrl_service.cameras_get_all()
        context['cameras'] = list(map_cameras_to_view_models(cameras))
        return context
