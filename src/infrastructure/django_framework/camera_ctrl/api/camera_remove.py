from django.http import HttpResponse, HttpResponseServerError
from django.views.generic import View

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException, CameraException
from camera_ctrl.api_exceptions import CameraNotFoundApiException


class CameraRemove(View):
    camera_ctrl_service: CameraCtrlService = None

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        try:
            self.camera_ctrl_service.camera_remove(camera_id=camera_id)
            return HttpResponse(status=204)

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)
