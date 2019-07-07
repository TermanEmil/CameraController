from django.http import HttpResponseNotFound


def camera_not_found(camera_port):
    return HttpResponseNotFound("Couldn't find a camera on port: {0}".format(camera_port))
