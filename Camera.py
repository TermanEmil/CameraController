import gphoto2 as gp


class Camera:
    def __init__(self, gp_camera, name='camera0'):
        assert isinstance(gp_camera, gp.Camera)

        self.gp_camera = gp_camera
        self.name = name
