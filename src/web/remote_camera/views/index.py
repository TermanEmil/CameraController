from business.CameraManager import CameraManager
from django.shortcuts import render
from .view_models import CameraViewModel


def index(request):
    context = {
        'cameras': [CameraViewModel(camera) for camera in CameraManager.instance().cameras]
    }

    return render(request, 'remote_camera/index.html', context)
