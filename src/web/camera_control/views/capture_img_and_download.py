import os
from time import time

from django.http import Http404, HttpResponse
from django.shortcuts import render

from factories import CameraManagerFactory
from .object_not_found import camera_not_found


def capture_img_and_download(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    storage_dir = '/tmp/'
    filename_prefix = 'img_{0}_{1}_{2}'.format(camera.name, camera_id, time())

    try:
        file_path = camera.capture_img(storage_dir, filename_prefix)
    except Exception as e:
        error = 'Internal error: {0}'.format(e)
        print(error)
        return render(request, 'camera_control/internal_error.html', {'error': error}, status=500)

    if not os.path.exists(file_path):
        return Http404()

    with open(file_path, 'rb') as fh:
        file_extension = os.path.splitext(file_path)[1][1:]
        download_filename = 'capture_sample{0}.{1}'.format(time(), file_extension)

        # I'm using this response as a blob inside an ajax request.
        # And the only easy way to get the filename from a blob, is to save it into content_type.
        response = HttpResponse(fh, content_type=download_filename)
        response['Content-Disposition'] = 'attachment;filename={0}'.format(download_filename)
        return response

