from django.shortcuts import render
from django_apscheduler.models import DjangoJob

from camera_control.models import CronTimelapse
from factories import ApSchedulerFactory, CameraManagerFactory
from forms import CronTimelapseForm
import os
from datetime import datetime


def timelapse_create(request):
    form = CronTimelapseForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        timelapse = form.save(commit=False)
        assert isinstance(timelapse, CronTimelapse)

        scheduler = ApSchedulerFactory.get()
        try:
            job = scheduler.add_job(
                take_photos,
                'cron',

                args=[timelapse],
                id=timelapse.name,

                year=timelapse.year,
                month=timelapse.month,
                day=timelapse.day,
                week=timelapse.week,
                day_of_week=timelapse.day_of_week,
                hour=timelapse.hour,
                minute=timelapse.minute,
                second=timelapse.second,

                start_date=timelapse.start_date,
                end_date=timelapse.end_date
            )

            django_job = DjangoJob.objects.get(name=job.id)
            timelapse.job = django_job
            timelapse.save()

            if not os.path.isdir(timelapse.storage_dir):
                os.makedirs(timelapse.storage_dir, exist_ok=True)

        except Exception as e:
            form.add_error(None, str(e))

    context = {
        'form': form
    }
    return render(request, 'camera_control/timelapse/timelapse_create.html', context)


def take_photos(timelapse: CronTimelapse):
    camera_manager = CameraManagerFactory.get()
    for i, camera in enumerate(camera_manager.cameras):
        filename = '{0}_{1}'.format(i, datetime.now())
        camera.capture_img(storage_dir=timelapse.storage_dir, filename_prefix=filename)
        print('Took photo with {0}'.format(camera.id))
    print('Finished taking photos\n')