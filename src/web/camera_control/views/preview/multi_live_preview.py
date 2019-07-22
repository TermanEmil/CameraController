from django.shortcuts import render

from factories import CameraManagerFactory


def multi_live_preview(request):
    context = {
        'cameras': [CameraViewModel(camera) for camera in CameraManagerFactory.get().cameras]
    }

    return render(request, 'camera_control/preview/multi_live_preview.html', context)


class CameraViewModel:
    def __init__(self, camera):
        self.name = camera.name
        self.id = camera.id