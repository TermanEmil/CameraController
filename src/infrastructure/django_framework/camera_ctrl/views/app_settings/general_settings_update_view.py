from django.urls import reverse_lazy
from django.views.generic import UpdateView

from camera_ctrl.models.app_settings_models import GeneralSettings


class GeneralSettingsUpdateView(UpdateView):
    model = GeneralSettings
    template_name = 'app_settings/general_settings.html'
    success_url = reverse_lazy('general_settings', kwargs={'pk': 1})

    fields = [
        'send_email_on_timelapse_error',
        'hard_reset_on_timelapse_error',
        'seconds_to_wait_after_hard_reset',
        'send_email_on_capture_error',
        'send_email_on_sync_error',
        'log_to_db_camera_capture',
        'autodetect_cameras_on_start',
        'emails',
        'email_subject_prefix']