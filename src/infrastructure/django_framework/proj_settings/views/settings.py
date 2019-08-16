from django.views.generic import TemplateView


class Settings(TemplateView):
    template_name = 'proj_settings/settings.html'
