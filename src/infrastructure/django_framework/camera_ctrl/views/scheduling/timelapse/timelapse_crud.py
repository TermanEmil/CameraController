from django.contrib import messages
from django.http import HttpResponse, HttpResponseServerError
from django.views.generic import CreateView, ListView, UpdateView, View

from adapters.scheduling.schedule_service import ScheduleService
from camera_ctrl.models import Timelapse, CronSchedule
from enterprise.scheduling import cron_schedule
from shared.di import obj_graph


class TimelapseCreate(CreateView):
    template_name = 'scheduling/timelapse/timelapse_create.html'

    model = Timelapse
    fields = ['name', 'storage_dir_format', 'filename_format', 'schedule', 'capture_index']
    success_message = 'Successfully created timelapse'

    schedule_service = obj_graph().provide(ScheduleService)

    def form_valid(self, form):
        response = super().form_valid(form)
        assert isinstance(self.object, Timelapse)

        schedule = CronSchedule.objects.filter(pk=self.object.schedule_id)
        if len(schedule) != 0:
            schedule = schedule[0]

            try:
                self.do_the_schedule_thing(schedule)
            except Exception as e:
                form.add_error(None, str(e))
                return super().form_invalid(form)

        messages.success(request=self.request, message=self.success_message)
        return response

    def do_the_schedule_thing(self, schedule: CronSchedule):
        dto = cron_schedule.CronSchedule(**vars(schedule))
        dto.pk = schedule.pk

        job_id = self.schedule_service.run_timelapse(self.object.pk, dto)
        self.object.schedule_job_id = job_id
        self.object.save()


class TimelapseList(ListView):
    template_name = 'scheduling/timelapse/timelapse_list.html'
    model = Timelapse


class TimelapseUpdate(UpdateView):
    template_name = 'scheduling/timelapse/timelapse_create.html'

    model = Timelapse
    fields = ['name', 'storage_dir_format', 'filename_format', 'schedule', 'capture_index']

    success_message = 'Timelapse successfully updated'
    schedule_service = obj_graph().provide(ScheduleService)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['updating'] = True
        return context

    def form_valid(self, form):
        previous_job_id = self.object.schedule_job_id

        response = super().form_valid(form)
        assert isinstance(self.object, Timelapse)

        try:
            if previous_job_id:
                self.schedule_service.delete_job(job_id=previous_job_id)
                self.object.schedule_job_id = None
                self.object.save()

            self.set_new_schedule_job()

        except Exception as e:
            form.add_error(None, str(e))
            return super().form_invalid(form)

        messages.success(request=self.request, message=self.success_message)
        return response

    def set_new_schedule_job(self):
        schedule = CronSchedule.objects.filter(pk=self.object.schedule_id)
        if len(schedule) == 0:
            return

        schedule = schedule[0]
        dto = cron_schedule.CronSchedule(**vars(schedule))
        dto.pk = schedule.pk

        job_id = self.schedule_service.run_timelapse(self.object.pk, dto)
        self.object.schedule_job_id = job_id
        self.object.save()


class TimelapseDelete(View):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs['pk']

        try:
            obj = Timelapse.objects.get(pk=pk)
            obj.delete()
        except Exception as e:
            return HttpResponseServerError(content=str(e))

        return HttpResponse(status=200)

