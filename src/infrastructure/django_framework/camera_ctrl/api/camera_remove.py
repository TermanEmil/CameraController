from django.http import HttpResponse, HttpResponseServerError, HttpResponseNotFound
from django.views.generic import View

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService, CameraNotFound


class CameraRemove(View):
    camera_ctrl_service: CameraCtrlService = None

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        try:
            self.camera_ctrl_service.camera_remove(camera_id=camera_id)
            return HttpResponse(status=200)

        except CameraNotFound as e:
            return HttpResponseNotFound(content=str(e))

        except Exception as e:
            return HttpResponseServerError(content=str(e))
