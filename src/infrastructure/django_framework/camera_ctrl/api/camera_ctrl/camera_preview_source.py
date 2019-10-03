from django.http import HttpResponseServerError, StreamingHttpResponse
from django.views.generic import View

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException, CameraException
from camera_ctrl.api_exceptions import CameraNotFoundApiException
from shared.di import obj_graph


class CameraPreviewSource(View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        return StreamingHttpResponse(
            self._preview_generator(camera_id=camera_id),
            content_type="multipart/x-mixed-replace;boundary=frame")

    def _preview_generator(self, camera_id):
        try:
            while True:
                frame = self\
                    .camera_ctrl_service\
                    .camera_capture_preview(camera_id=camera_id)

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n'
                       + frame.tobytes()
                       + b'\r\n')

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
