from django.views.generic import TemplateView
from mapper.object_mapper import ObjectMapper

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from ..view_models.camera_view_model import CameraViewModel


class Index(TemplateView):
    template_name = 'camera_ctrl/index.html'

    camera_ctrl_service: CameraCtrlService = None
    obj_mapper: ObjectMapper = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        cameras = self.camera_ctrl_service.cameras_get_all()
        context['cameras'] = (self.obj_mapper.map(camera, CameraViewModel) for camera in cameras)
        return context
