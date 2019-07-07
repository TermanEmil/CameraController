import asyncio
import logging
import sys
import time

import gphoto2 as gp
from django.http import StreamingHttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.views.decorators import gzip

from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from . import view_models
from PIL import Image
import io
import timeit


from .forms import PreviewSettingsForm


def index(request):
    camera_manager = CameraManager.instance()
    camera_manager.disconnect_all_cameras()
    camera_manager.autodetect_all_cameras()

    # camera_manager.cameras = [
    #     CameraWrapper(gp.Camera(), camera_name='Nikon 6_1', port='usb00,020'),
    #     CameraWrapper(gp.Camera(), camera_name='Nikon 6_2', port='usb00,030'),
    # ]

    context = {
        'cameras': [view_models.CameraViewModel(camera) for camera in camera_manager.cameras]
    }

    return render(request, 'remote_camera/index.html', context)


def live_preview(request, camera_port):
    if request.method == 'POST':
        form = PreviewSettingsForm(request.POST)
        if form.is_valid():
            request.session['preview_quality'] = form.quality

    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return HttpResponseNotFound(b"Couldn't find a camera on the specified port")

    context = {
        'camera_port': camera_port,
        'form': PreviewSettingsForm()
    }
    return render(request, 'remote_camera/live_preview.html', context)


def _live_preview_frame_generator(camera):
    assert isinstance(camera, CameraWrapper)

    try:
        while True:
            frame = camera.capture_preview()

            img = Image.open(io.BytesIO(frame))
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='JPEG', optimize=True, quality=10)

            frame = img_byte_array.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        logging.error('Failed to live stream: {0}'.format(e))


@gzip.gzip_page
def live_preview_source(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return HttpResponseNotFound(b"Couldn't find a camera on the specified port")

    return StreamingHttpResponse(
        _live_preview_frame_generator(camera),
        content_type="multipart/x-mixed-replace;boundary=frame")
