from django.http import HttpResponseNotFound


class CameraNotFoundApiException(HttpResponseNotFound):
    def __init__(self, camera_id: str):
        msg = 'Camera with Id {} not found'.format(camera_id)
        super().__init__(content=msg)
