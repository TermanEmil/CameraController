from django.shortcuts import render

from .view_models import CameraViewModel
from factories import CameraManagerFactory


def multi_live_preview(request):
    context = {
        'cameras': [CameraViewModel(camera) for camera in CameraManagerFactory.get().cameras]
    }

    return render(request, 'camera_control/multi_live_preview.html', context)