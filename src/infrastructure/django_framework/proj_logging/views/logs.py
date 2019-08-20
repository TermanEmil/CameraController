from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, View

from proj_logging.models import HistoryUnit


class LogsList(ListView):
    model = HistoryUnit
    template_name = 'proj_logging/logs_list.html'
    paginate_by = 30
    ordering = ['-created_time']

    def get_queryset(self):
        log_type = self.request.GET.get('log_type', None)
        search = self.request.GET.get('search', None)

        objs = super().get_queryset()

        if log_type:
            objs = objs.filter(log_type=log_type)

        if search:
            objs = objs.filter(content__icontains=search)

        return objs


class LogsDelete(DeleteView):
    model = HistoryUnit
    success_url = reverse_lazy('all_logs')


class LogsDeleteAll(View):
    def dispatch(self, request, *args, **kwargs):
        HistoryUnit.objects.all().delete()
        return redirect(reverse_lazy('all_logs'))