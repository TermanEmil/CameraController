from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from shared.di import obj_graph
from ._utils import map_cameras_to_view_models


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'camera_ctrl/index.html'

    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cameras = self.camera_ctrl_service.cameras_get_all()
        camera_view_models = list(map_cameras_to_view_models(cameras))
        context['cameras'] = camera_view_models
        return context

