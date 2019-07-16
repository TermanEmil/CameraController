from django.shortcuts import render

from factories import CameraManagerFactory
from .object_not_found import camera_not_found
from time import time
import os
from mimetypes import guess_type
from django.http import Http404, HttpResponse
import ntpath


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
        return render(request, 'camera_control/internal_error.html', {'error': error}, status=500)

    if not os.path.exists(file_path):
        return Http404()

    with open(file_path, 'rb') as fh:
        response = HttpResponse(fh, content_type=guess_type(file_path))

        file_extension = os.path.splitext(file_path)[1][1:]
        download_filename = 'capture_sample{0}.{1}'.format(time(), file_extension)
        response['Content-Disposition'] = 'attachment;filename={0}'.format(download_filename)
        return response

