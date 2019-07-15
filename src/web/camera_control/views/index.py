from django.shortcuts import render

from factories import CameraManagerFactory
from .view_models import CameraViewModel


def index(request):
    camera_manager = CameraManagerFactory.get()
    context = {
        'cameras': [CameraViewModel(camera) for camera in camera_manager.cameras]
    }

    return render(request, 'camera_control/index.html', context)
