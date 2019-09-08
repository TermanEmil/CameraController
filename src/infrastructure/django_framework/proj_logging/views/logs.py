from django.db.models import F, Sum
from django.db.models.functions import Concat
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView, View

from proj_logging.filters.log_filter import LogFilter
from proj_logging.models import HistoryUnit


class LogsList(ListView):
    model = HistoryUnit
    template_name = 'proj_logging/logs_list.html'
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