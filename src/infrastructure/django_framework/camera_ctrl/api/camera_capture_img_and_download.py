from django.http import HttpResponseServerError, FileResponse
from django.views.generic import View

from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException, CameraException
from camera_ctrl.api_exceptions import CameraNotFoundApiException


class CameraCaptureImgAndDownload(View):
    camera_ctrl_service: CameraCtrlService = None

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']

        try:
            capture_dto = self\
                .camera_ctrl_service\
                .camera_capture_img_and_download(camera_id=camera_id)

            return FileResponse(
                open(capture_dto.real_file_path, 'rb'),
                content_type=capture_dto.download_filename)

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
