from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseServerError, HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View, DeleteView

from business.scheduling.scheduler import Scheduler
from camera_ctrl.models import CronSchedule
from enterprise.scheduling import cron_schedule
from shared.di import obj_graph
from shared.utils.hard_map_objects import hard_map_objects


class CronScheduleCreate(SuccessMessageMixin, CreateView):
    model = CronSchedule

    template_name = 'scheduling/cron/cron_schedule_create.html'
    fields = [
        'name',
        'start_date', 'end_date',
        'year', 'month', 'day', 'week', 'day_of_week',
        'hour', 'minute', 'second']

    success_message = 'Schedule successfully created'

    def get_initial(self):
        initial_values = cron_schedule.CronSchedule()
        return vars(initial_values)


class CronScheduleList(ListView):
    model = CronSchedule
    template_name = 'scheduling/cron/cron_schedule_list.html'


class CronScheduleUpdate(UpdateView):
    model = CronSchedule
    template_name = 'scheduling/cron/cron_schedule_create.html'

    success_message = 'Schedule successfully updated'

    fields = [
        'name',
        'start_date', 'end_date',
        'year', 'month', 'day', 'week', 'day_of_week',
        'hour', 'minute', 'second']

    scheduler = obj_graph().provide(Scheduler)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['updating'] = True
        return context

    def form_valid(self, form):
        response = super().form_valid(form)

        schedule = cron_schedule.CronSchedule(**vars(self.object))
        hard_map_objects(self.object, schedule)

        try:
            self.scheduler.modify(schedule)
        except Exception as e:
            form.add_error(None, str(e))
            return super().form_invalid(form)

        messages.success(self.request, self.success_message)
        return response


class CronScheduleDelete(DeleteView):
    model = CronSchedule
    scheduler = obj_graph().provide(Scheduler)

    def get(self, request, *args, **kwargs):
        try:
            obj = self.get_object()
            self.scheduler.delete(obj.pk)
            obj.delete()

        except Exception as e:
            return HttpResponseServerError(content=str(e))

        return HttpResponse(status=200)