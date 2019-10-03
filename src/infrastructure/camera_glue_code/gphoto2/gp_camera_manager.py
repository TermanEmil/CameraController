from threading import Lock
from typing import Dict

import gphoto2 as gp
import atexit

from enterprise.camera_ctrl.camera import Camera
from enterprise.camera_ctrl.camera_manager import CameraManager
from enterprise.camera_ctrl.multi_lock import MultiLock
from infrastructure.camera_glue_code.gphoto2.gp_camera import GpCamera


class GpCameraManager(CameraManager):
    def __init__(self):
        self._gp_lock = Lock()
        self._cameras_dict_lock = Lock()

        gp.check_result(gp.use_python_logging())
        self._cameras_dict: Dict[str, GpCamera] = {}
        atexit.register(self.disconnect_all)

    @property
    def all_locks(self) -> MultiLock:
        return MultiLock([self.sync_lock])

    @property
    def sync_lock(self) -> Lock:
        return self._gp_lock

    @property
    def cameras(self) -> iter:
        with self._cameras_dict_lock:
            return list(self._cameras_dict.values())

    def detect_all_cameras(self):
        self.disconnect_all()

        with self._gp_lock:
            cameras_name_and_port = gp.check_result(gp.gp_camera_autodetect())

            # Search ports for camera port name
            port_info_list = gp.PortInfoList()
            port_info_list.load()

            for name, port in cameras_name_and_port:
                gp_camera = gp.Camera()
                idx = port_info_list.lookup_path(port)
                port_info = port_info_list[idx]
                gp_camera.set_port_info(port_info)

                try:
                    camera = GpCamera(
                        name=name,
                        port=port,
                        gp_camera=gp_camera,
                        lock=self.sync_lock)

                    with self._cameras_dict_lock:
                        self._cameras_dict[camera.id] = camera

                except Exception as e:
                    print('Detect all: {0}'.format(e))

    def get_camera(self, camera_id) -> Camera:
        with self._cameras_dict_lock:
            return self._cameras_dict.get(camera_id)

    def remove_camera(self, camera_id):
        with self._cameras_dict_lock:
            if camera_id not in self._cameras_dict:
                return

            camera = self._cameras_dict[camera_id]
            camera.disconnect()

            self._cameras_dict.pop(camera_id)

    def disconnect_all(self):
        camera_ids = [camera.id for camera in self.cameras]
        for camera_id in camera_ids:
            self.remove_camera(camera_id)

