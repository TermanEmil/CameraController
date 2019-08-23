from django.views.generic import View
from django.http import HttpResponse, HttpResponseServerError
from adapters.camera.ctrl.camera_ctrl_service import CameraCtrlService
from proj_settings.settings_facade import SettingsFacade


class CamerasHardResetAll(View):
    camera_ctrl_service: CameraCtrlService = None

    def get(self, request):
        try:
            settings = SettingsFacade()
            self.camera_ctrl_service.hard_reset_all_cameras(
                wait_seconds_after_reset=settings.seconds_to_wait_after_hard_reset)
            return HttpResponse(status=200)

        except IOError as e:
            return HttpResponseServerError(content='ykush program is probably not installed: {}'.format(e))
        except Exception as e:
            return HttpResponseServerError(content=str(e))
