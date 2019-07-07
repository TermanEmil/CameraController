from django.shortcuts import render


def camera_not_found(request, camera_port):
    context = {
        'camera_port': camera_port
    }

    return render(request, 'remote_camera/camera_not_found.html', context)
