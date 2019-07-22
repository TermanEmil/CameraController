from django.shortcuts import render

from factories import CameraManagerFactory


def index(request):
    camera_manager = CameraManagerFactory.get()
    context = {
        'cameras': [CameraViewModel(camera) for camera in camera_manager.cameras]
    }

    return render(request, 'camera_control/index.html', context)


class CameraViewModel:
    def __init__(self, camera):
        self.name = camera.name
        self.id = camera.id
        self.summary = camera.summary