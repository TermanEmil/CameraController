from django.http import StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators import gzip

from CameraManager import CameraManager
from CameraWrapper import CameraWrapper
from . import view_models


def gen(camera):
    assert isinstance(camera, CameraWrapper)

    try:
        while True:
            frame = camera.capture_preview()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    except Exception as e:
        print(e)


def index(request):
    camera_manager = CameraManager.instance()
    camera_manager.disconnect_all_cameras()
    camera_manager.autodetect_all_cameras()

    context = {
        'cameras': [view_models.CameraViewModel(camera) for camera in camera_manager.cameras]
    }

    return render(request, 'remote_camera/index.html', context)


def give_me_da_preview(request):
    return render(request, 'remote_camera/live_preview.html')


@gzip.gzip_page
def live_preview(request):
    camera = CameraManager.instance().cameras[0]
    return StreamingHttpResponse(gen(camera), content_type="multipart/x-mixed-replace;boundary=frame")
