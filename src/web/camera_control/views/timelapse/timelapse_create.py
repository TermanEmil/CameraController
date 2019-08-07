import os
import sys
import threading
from datetime import datetime

from django.shortcuts import render

from camera_control.models import CronTimelapse
from factories import ApSchedulerFactory, CameraManagerFactory
from forms import CronTimelapseForm
from business.camera_control.camera import Camera


def timelapse_create(request):
    form = CronTimelapseForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        timelapse_model = form.save(commit=False)
        assert isinstance(timelapse_model, CronTimelapse)

        try:
            timelapse_model.save()
            _create_schedule_job(timelapse_model)

        except Exception as e:
            if timelapse_model.pk is not None:
                timelapse_model.delete()

            form.add_error(None, str(e))

    context = {
        'form': form
    }
    return render(request, 'camera_control/timelapse/timelapse_create.html', context)


def _create_schedule_job(timelapse: CronTimelapse):
    scheduler = ApSchedulerFactory.get()

    return scheduler.add_job(
        take_photos,
        'cron',

        args=[timelapse],
        id=str(timelapse.pk),

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


def take_photos(timelapse: CronTimelapse):
    timelapse.refresh_from_db()

    now = datetime.now()
    camera_manager = CameraManagerFactory.get()

    img_capture_tasks = []
    for camera in camera_manager.cameras:
        storage_dir = apply_naming_tricks(
            name_format=timelapse.storage_dir_format,
            time=now,
            timelapse=timelapse,
            camera=camera
        )

        filename = apply_naming_tricks(
            name_format=timelapse.filename_format,
            time=now,
            timelapse=timelapse,
            camera=camera
        )

        try:
            if not os.path.isdir(storage_dir):
                os.makedirs(storage_dir, exist_ok=True)
        except Exception as e:
            print('Failed to create directory {}: {}'.format(storage_dir, e), file=sys.stderr)
            continue

        img_capture_tasks.append(threading.Thread(target=_capture_picture, args=(camera, storage_dir, filename,)))

    for capture_task in img_capture_tasks:
        capture_task.start()

    for capture_task in img_capture_tasks:
        capture_task.join()

    print('{}: Capture index: {} --- Finished taking photos\n'.format(timelapse.name, timelapse.capture_index))
    timelapse.capture_index += 1
    timelapse.save()


def _capture_picture(camera, storage_dir, filename):
    camera.capture_img(storage_dir=storage_dir, filename_prefix=filename)
    print('Took photo with {}'.format(camera.id))


class LazyFormatDictIgnoreMissing(dict):
    def __getitem__(self, key):
        func = dict.__getitem__(self, key)

        if callable(func):
            return func()

        return super().__getitem__(key)

    def __missing__(self, key):
        return '{' + key + '}'


# Use lazy dictionary values because some of these values may be computing intensive and may not even be used.
def apply_naming_tricks(name_format, time: datetime, timelapse: CronTimelapse, camera: Camera):
    format_args = LazyFormatDictIgnoreMissing({
        'timestamp': lambda: time.timestamp() * 1000,
        'time': lambda: time,
        'capture_index': lambda: timelapse.capture_index,

        'camera_id': lambda: camera.id,
        'camera_serial_nb': lambda: camera.serial_nb,
        'camera_name': lambda: camera.name,

        'timelapse_name': lambda: timelapse.name,
        'timelapse_id': lambda: timelapse.pk
    })

    return name_format.format_map(format_args)
