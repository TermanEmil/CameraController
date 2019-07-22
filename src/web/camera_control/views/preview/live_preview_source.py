import io

from PIL import Image
from django.http import StreamingHttpResponse

from business.camera_control.camera import Camera
from factories import CameraManagerFactory
from views.object_not_found import camera_not_found


def live_preview_source(request, camera_id):
    camera = CameraManagerFactory.get().get_camera(camera_id)
    if camera is None:
        return camera_not_found(request, camera_id)

    return StreamingHttpResponse(
        _live_preview_frame_generator(camera),
        content_type="multipart/x-mixed-replace;boundary=frame"
    )


def _live_preview_frame_generator(camera: Camera):
    try:
        while True:
            frame = camera.capture_preview()

            img = Image.open(io.BytesIO(frame))
            img_byte_array = io.BytesIO()
            img.save(img_byte_array, format='JPEG')

            frame = img_byte_array.getvalue()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    except Exception as e:
        print('Live preview source: Exception: {0}'.format(e))
