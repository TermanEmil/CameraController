from django.views.generic import TemplateView
from mapper.object_mapper import ObjectMapper

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from ..view_models.camera_view_model import CameraViewModel


class MultiPreview(TemplateView):
    template_name = 'camera_ctrl/multi_preview.html'

    camera_ctrl_service: CameraCtrlService = None
    obj_mapper: ObjectMapper = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            cameras = self.camera_ctrl_service.cameras_get_all()
            camera_view_models = (self.obj_mapper.map(camera, CameraViewModel) for camera in cameras)
            context['cameras'] = camera_view_models

        except Exception as e:
            context['error'] = str(e)

        return context
