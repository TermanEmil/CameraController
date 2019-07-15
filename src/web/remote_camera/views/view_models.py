from business.camera_wrapper import CameraWrapper


class CameraViewModel:
    def __init__(self, camera):
        assert isinstance(camera, CameraWrapper)

        self.name = camera.name
        self.port = camera.port
        self.summary = camera.serial_nb
