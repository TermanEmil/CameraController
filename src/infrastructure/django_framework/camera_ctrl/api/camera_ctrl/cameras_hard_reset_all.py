from django.http import HttpResponse, HttpResponseServerError
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException, CameraResetException
from shared.di import obj_graph


class CamerasHardResetAll(LoginRequiredMixin, View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get(self, request):
        try:
            self.camera_ctrl_service.hard_reset_all_cameras()
            return HttpResponse(status=200)

        except CameraResetException as e:
            return HttpResponseServerError(content=str(e))

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
