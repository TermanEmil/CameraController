from typing import Iterable

from shared.utils.hard_map_objects import hard_map_objects
from ..view_models import CameraViewModel


def map_camera_to_view_model(camera):
    model = CameraViewModel()
    hard_map_objects(camera, model)

    return model


def map_cameras_to_view_models(cameras: Iterable[object]):
    for camera in cameras:
        yield map_camera_to_view_model(camera)

