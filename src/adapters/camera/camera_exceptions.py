from business.camera import exceptions


class CameraNotFound(Exception):
    def __init__(self, original: exceptions.CameraNotFound):
        super().__init__(str(original))