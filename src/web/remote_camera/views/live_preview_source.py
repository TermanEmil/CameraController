import io
import logging

from PIL import Image
from business.CameraManager import CameraManager
from business.CameraWrapper import CameraWrapper
from django.http import StreamingHttpResponse
from django.views.decorators import gzip

from .camera_not_found import camera_not_found
from ..utils.settings_manager import SettingsManager


@gzip.gzip_page
def live_preview_source(request, camera_port):
    camera = CameraManager.instance().get_camera_on_port(camera_port)
    if camera is None:
        return camera_not_found(request, camera_port)

    camera_settings = SettingsManager(request.session).get_settings(camera)
    quality = camera_settings.quality

    return StreamingHttpResponse(
        _live_preview_frame_generator(camera, quality),
        content_type="multipart/x-mixed-replace;boundary=frame")


def _live_preview_frame_generator(camera, quality):
    assert isinstance(camera, CameraWrapper)
    assert 1 <= quality <= 100

    try:
        while True:
            frame = camera.capture_preview()

            img = Image.open(io.BytesIO(frame))
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='JPEG', optimize=True, quality=quality)

            frame = img_byte_array.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        logging.error('Failed to live stream: {0}'.format(e))
