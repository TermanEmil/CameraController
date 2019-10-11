from django.http import HttpResponse, HttpResponseServerError
from django.views.generic import View

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException, CameraException
from camera_ctrl.api_exceptions import CameraNotFoundApiException
from shared.di import obj_graph


class CameraReconnect(View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        try:
            self.camera_ctrl_service.camera_reconnect(camera_id=camera_id)
            return HttpResponse(status=200)

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
