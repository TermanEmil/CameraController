from django.db.models import F
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, View

from camera_ctrl.filters.app_logging import LogFilter
from camera_ctrl.models import HistoryUnit


class LogsList(ListView):
    model = HistoryUnit
    template_name = 'app_logging/logs_list.html'
    paginate_by = 30
    allow_empty = True
    ordering = ['-created_time']

    def get_queryset(self):
        objs = super().get_queryset().annotate(
            title_content=Concat(F('title'), F('content')))

        filtered_logs = LogFilter(self.request.GET, queryset=objs)
        return filtered_logs.qs


class LogsDelete(DeleteView):
    model = HistoryUnit
    success_url = reverse_lazy('all_logs')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class LogsDeleteAll(View):
    def dispatch(self, request, *args, **kwargs):
        HistoryUnit.objects.all().delete()
        return redirect(reverse_lazy('all_logs'))