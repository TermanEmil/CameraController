from ..camera import Camera
from ..camera_config import CameraConfig, CameraConfigField
from PIL import Image, ImageDraw
import io


class StubCamera(Camera):
    def __init__(self, name, camera_id, summary, config: CameraConfig):
        self._name = name
        self._summary = summary
        self._id = camera_id
        self._config = config

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @property
    def summary(self):
        return self._summary

    def list_configs(self):
        if self._config is None:
            return []

        assert isinstance(self._config, CameraConfig)
        for field_id, field in self._config.all_fields.items():
            assert isinstance(field, CameraConfigField)
            yield field.name

    def get_config(self) -> CameraConfig:
        return self._config

    def get_single_config(self, config_name) -> CameraConfigField:
        return self._config.all_fields.get(config_name)

    def set_config(self, config_fields: iter):
        pass

    def capture_preview(self) -> memoryview:
        # Draw 2 triangles
        img = Image.new('RGB', (255, 255))
        draw = ImageDraw.Draw(img)
        draw.polygon([(20, 10), (200, 200), (100, 20)], fill=(255, 0, 0))
        draw.polygon([(200, 10), (200, 200), (150, 50)], fill='yellow')

        img_bytes_array = io.BytesIO()
        img.save(img_bytes_array, format='JPEG')
        return memoryview(img_bytes_array.getvalue())