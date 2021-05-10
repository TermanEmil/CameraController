from django.http import HttpResponseBadRequest, HttpResponse, HttpResponseServerError
from django.views import View

from adapters.camera.configs.camera_config_service import CameraConfigService
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraNotFoundException, CameraException, InvalidConfigException
from camera_ctrl.api_exceptions import CameraNotFoundApiException
from shared.di import obj_graph


class CameraGetConfigView(View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)
    camera_config_service = obj_graph().provide(CameraConfigService)

    def get(self, request, *args, **kwargs):
        camera_id = kwargs['camera_id']
        config_name = kwargs['config_name']

        try:
            if camera_id.lower() == 'first':
                camera = self.camera_ctrl_service.cameras_get_first()
                if camera is None:
                    raise CameraNotFoundException()
                camera_id = camera.id

            config = self.camera_config_service.get_config(camera_id=camera_id, config_name=config_name)
            return HttpResponse(content=config.value)

        except CameraNotFoundException:
            return CameraNotFoundApiException(camera_id=camera_id)

        except InvalidConfigException as e:
            return HttpResponseBadRequest(content=str(e))

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
