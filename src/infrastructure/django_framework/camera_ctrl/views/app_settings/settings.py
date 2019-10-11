from django.views.generic import TemplateView

from camera_ctrl.models.app_settings_models import GeneralSettings


class Settings(TemplateView):
    template_name = 'app_settings/settings.html'

    def get(self, request, *args, **kwargs):
        GeneralSettings.load()
        return super().get(request, *args, **kwargs)