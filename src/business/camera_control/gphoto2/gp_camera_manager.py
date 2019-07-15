from threading import Lock

import gphoto2 as gp

from .gp_camera import GpCamera
from ..camera import Camera
from ..camera_manager import CameraManager


class GpCameraManager(CameraManager):
    def __init__(self):
        self._gp_lock = Lock()

        gp.check_result(gp.use_python_logging())
        self._cameras_dict = {}

    def detect_all_cameras(self):
        self.disconnect_all()

        with self._gp_lock:
            cameras_name_and_port = gp.check_result(gp.gp_camera_autodetect())

        # Search ports for camera port name
        port_info_list = gp.PortInfoList()

        with self._gp_lock:
            port_info_list.load()

        for name, port in cameras_name_and_port:
            with self._gp_lock:
                gp_camera = gp.Camera()
                idx = port_info_list.lookup_path(port)
                gp_camera.set_port_info(port_info_list[idx])

            try:
                camera = GpCamera(name=name, port=port, gp_camera=gp_camera, gp_lock=self._gp_lock)
                self._cameras_dict[camera.id] = camera
            except Exception as e:
                print('Detect all: {0}'.format(e))

    @property
    def cameras(self) -> iter:
        return self._cameras_dict.values()

    def get_camera(self, camera_id) -> Camera:
        return self._cameras_dict.get(camera_id)

    def disconnect_all(self):
        print('Disconnecting from all cameras...')
        for camera in self.cameras:
            assert isinstance(camera, GpCamera)
            camera.disconnect()

        self._cameras_dict.clear()
        print('Disconnected from all cameras')

