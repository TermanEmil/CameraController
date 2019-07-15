from django.shortcuts import render

from .view_models import CameraViewModel
from ..factories import CameraManagerFactory


def index(request):
    context = {
        'cameras': [CameraViewModel(camera) for camera in CameraManagerFactory.get().cameras]
    }

    return render(request, 'remote_camera/index.html', context)
