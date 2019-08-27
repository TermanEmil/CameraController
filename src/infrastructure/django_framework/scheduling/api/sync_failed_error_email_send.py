import logging

from django.core.mail import send_mail
from django.http import HttpResponse, HttpResponseNotFound
from django.views.generic import View

from proj_settings.settings_facade import SettingsFacade


class SyncFailedErrorEmailSend(View):
    def get(self, request, *args, **kwargs):
        settings = SettingsFacade()
        if not settings.send_email_on_sync_error:
            return

        try:
            send_mail(
                subject='Failed to sync folders',
                message='Failed to sync the Timelapse folders.',
                recipient_list=list(settings.emails),
                fail_silently=False,
                from_email=None)
            return HttpResponse(status=200)

        except Exception as e:
            logging.error('Failed to send emails. Error: {}'.format(e))
            return HttpResponseNotFound(content=str(e))

