from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException
from camera_ctrl.api_exceptions import CameraNotFoundApiException
from shared.di import obj_graph


class CameraRemove(LoginRequiredMixin, View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        try:
            self.camera_ctrl_service.camera_remove(camera_id=camera_id)
            return HttpResponse(status=204)

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)
