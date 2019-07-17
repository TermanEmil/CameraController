from ..camera import Camera
from ..camera_config import CameraConfig, CameraConfigField
from PIL import Image, ImageDraw
import io
import os


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
        img = self._stub_img()

        img_bytes_array = io.BytesIO()
        img.save(img_bytes_array, format='JPEG')
        return memoryview(img_bytes_array.getvalue())

    def capture_img(self, storage_dir, filename_prefix) -> str:
        if not os.path.isdir(storage_dir):
            raise Exception('Path: "{0}" does not exist'.format(storage_dir))

        img = self._stub_img()
        filename = '{0}.jpeg'.format(filename_prefix)
        file_path = os.path.join(storage_dir, filename)

        img.save(file_path, format='JPEG')
        return file_path

    def disconnect(self):
        pass

    @staticmethod
    def _stub_img():
        # Draw 2 triangles
        img = Image.new('RGB', (255, 255))
        draw = ImageDraw.Draw(img)
        draw.polygon([(20, 10), (200, 200), (100, 20)], fill=(255, 0, 0))
        draw.polygon([(200, 10), (200, 200), (150, 50)], fill='yellow')

        return img