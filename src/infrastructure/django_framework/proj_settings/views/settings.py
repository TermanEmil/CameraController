from django.views.generic import TemplateView

from proj_settings.models import GeneralSettings


class Settings(TemplateView):
    template_name = 'proj_settings/settings.html'

    def get(self, request, *args, **kwargs):
        GeneralSettings.load()
        return super().get(request, *args, **kwargs)