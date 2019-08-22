from django.urls import reverse_lazy
from django.views.generic import UpdateView

from proj_settings.models import GeneralSettings


class GeneralSettingsUpdateView(UpdateView):
    model = GeneralSettings
    template_name = 'proj_settings/general_settings.html'
    success_url = reverse_lazy('general_settings', kwargs={'pk': 1})

    fields = [
        'send_email_on_error',
        'log_to_db_timelapse_capture',
        'log_to_db_camera_capture',
        'autodetect_cameras_on_start',
        'emails']