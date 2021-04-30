from django.forms import inlineformset_factory
from django.views.generic import CreateView, ListView

from adapters.scheduling.schedule_service import ScheduleService
from camera_ctrl.models.scheduling_models import ScheduledConfig, ScheduledConfigField, CronSchedule
from enterprise.scheduling import cron_schedule
from shared.di import obj_graph

ScheduledConfigFieldFormSet = inlineformset_factory(
    ScheduledConfig,
    ScheduledConfigField,
    fields=('name', 'value'))


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
