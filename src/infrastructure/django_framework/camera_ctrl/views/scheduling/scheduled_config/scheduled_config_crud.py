from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponseServerError, HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView

from adapters.scheduling.schedule_service import ScheduleService
from camera_ctrl.models.scheduling_models import ScheduledConfig, ScheduledConfigField, CronSchedule
from enterprise.scheduling import cron_schedule
from shared.di import obj_graph

ScheduledConfigFieldFormSet = inlineformset_factory(
    ScheduledConfig,
    ScheduledConfigField,
    fields=('name', 'value'),
    extra=1)


class ScheduledConfigCreate(CreateView):
    model = ScheduledConfig
    fields = ['name', 'schedule']
    template_name = 'scheduling/scheduled_config/scheduled_config_create.html'
    schedule_service = obj_graph().provide(ScheduleService)

    def get_context_data(self, **kwargs):
        # we need to overwrite get_context_data
        # to make sure that our formset is rendered
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['fields'] = ScheduledConfigFieldFormSet(self.request.POST)
        else:
            data['fields'] = ScheduledConfigFieldFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        fields = context['fields']

        self.object = form.save()
        if fields.is_valid():
            fields.instance = self.object
            fields.save()
        else:
            return super().form_invalid(form)

        response = super().form_valid(form)
        schedules = CronSchedule.objects.filter(pk=self.object.schedule_id)
        if len(schedules) != 0:
            schedule = schedules[0]

            try:
                self.do_the_schedule_thing(schedule)
            except Exception as e:
                form.add_error(None, str(e))
                return super().form_invalid(form)

        return response

    def do_the_schedule_thing(self, schedule: CronSchedule):
        dto = cron_schedule.CronSchedule(**vars(schedule))
        dto.pk = schedule.pk

        job_id = self.schedule_service.run_scheduled_config(self.object.pk, dto)
        self.object.schedule_job_id = job_id
        self.object.save()


class ScheduledConfigList(ListView):
    template_name = 'scheduling/scheduled_config/scheduled_config_list.html'
    model = ScheduledConfig


class ScheduledConfigUpdate(UpdateView):
    model = ScheduledConfig
    schedule_service = obj_graph().provide(ScheduleService)
    success_message = 'Scheduled Config successfully updated'
    template_name = 'scheduling/scheduled_config/scheduled_config_create.html'

    fields = ['name', 'schedule']

    def get_context_data(self, **kwargs):
        scheduled_config = ScheduledConfig.objects.get(id=self.kwargs['pk'])
        context = super().get_context_data(**kwargs)
        context['updating'] = True

        if self.request.POST:
            context['fields'] = ScheduledConfigFieldFormSet(self.request.POST, instance=scheduled_config)
        else:
            context['fields'] = ScheduledConfigFieldFormSet(instance=scheduled_config)

        return context

    def form_valid(self, form):
        previous_job_id = self.object.schedule_job_id

        context = self.get_context_data()
        fields = context['fields']

        self.object = form.save()
        if fields.is_valid():
            fields.instance = self.object
            fields.save()
        else:
            return super().form_invalid(form)

        response = super().form_valid(form)

        try:
            if previous_job_id:
                self.schedule_service.delete_job(job_id=previous_job_id)

            self._reschedule_job()

        except Exception as e:
            form.add_error(None, str(e))
            return super().form_invalid(form)

        messages.success(request=self.request, message=self.success_message)
        return response

    def _reschedule_job(self):
        schedule = CronSchedule.objects.filter(pk=self.object.schedule_id)
        if len(schedule) == 0:
            return

        schedule = schedule[0]
        dto = cron_schedule.CronSchedule(**vars(schedule))
        dto.pk = schedule.pk

        job_id = self.schedule_service.run_scheduled_config(self.object.pk, dto)
        self.object.schedule_job_id = job_id
        self.object.save()


class ScheduledConfigDelete(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            obj = ScheduledConfig.objects.get(pk=pk)
            obj.delete()
        except Exception as e:
            return HttpResponseServerError(content=str(e))

        return HttpResponse(status=200)