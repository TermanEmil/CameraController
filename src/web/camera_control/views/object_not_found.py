from django.shortcuts import render


def object_not_found(request, message):
    context = {
        'msg': message,
    }

    return render(request, 'camera_control/object_not_found.html', context, status=404)


def camera_not_found(request, camera_id):
    msg = 'Could not find a camera with id = {0}'.format(camera_id)
    return object_not_found(request, msg)
