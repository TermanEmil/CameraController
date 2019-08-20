from django.views.generic import TemplateView


class ProjLoggingSettings(TemplateView):
    template_name = 'proj_settings/proj_logging_settings.html'

    def dispatch(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)