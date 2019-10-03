from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from business.camera.exceptions import CameraException, HardResetException
from proj_settings.settings_facade import SettingsFacade
from shared.di import obj_graph


class CamerasHardResetAll(View):
    camera_ctrl_service = obj_graph().provide(CameraCtrlService)

    def get(self, request):
        try:
            settings = SettingsFacade()
            time_to_wait = settings.seconds_to_wait_after_hard_reset

            self.camera_ctrl_service\
                .hard_reset_all_cameras(wait_seconds_after_reset=time_to_wait)

            return HttpResponse(status=200)

        except HardResetException as e:
            return HttpResponseServerError(content=str(e))

        except CameraException as e:
            return HttpResponseServerError(content=str(e))
