from mapper.object_mapper import ObjectMapper

from adapters.camera.ctrl.camera_ctrl_service import CameraDto
from .view_models.camera_view_model import CameraViewModel


class AppObjectMapper(ObjectMapper):
    def __init__(self):
        super().__init__()

        self.create_map(CameraDto, CameraViewModel)