from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException


class CamerasAutodetect(View):
    camera_ctrl_service: CameraCtrlService = None

    def get(self, request):
        try:
            self.camera_ctrl_service.cameras_autodetect()
            return HttpResponse(status=200)

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
