import gphoto2 as gp
import atexit
from threading import Thread
from .CameraWrapper import CameraWrapper


class CameraManager:
    _instance = None

    def __init__(self):
        self.cameras = []
        gp.check_result(gp.use_python_logging())

        atexit.register(self.disconnect_all_cameras)

    @staticmethod
    def instance():
        if CameraManager._instance is None:
            CameraManager._instance = CameraManager()

        return CameraManager._instance

    def autodetect_all_cameras(self):
        cameras_name_and_port = gp.check_result(gp.gp_camera_autodetect())

        # Search ports for camera port name
        port_info_list = gp.PortInfoList()
        port_info_list.load()

        camera_wrappers = []
        for name, port in cameras_name_and_port:
            print('Detected camera {0} on port: {1}'.format(name, port))

            camera = gp.Camera()
            idx = port_info_list.lookup_path(port)
            camera.set_port_info(port_info_list[idx])

            cam_wrapper = CameraWrapper(camera, camera_name=name, port=port)

            camera_wrappers.append(cam_wrapper)

        print('Detected a total of {0} camera(s)\n'.format(len(camera_wrappers)))
        self.cameras = camera_wrappers

    def disconnect_all_cameras(self):
        for camera in self.cameras:
            assert isinstance(camera, CameraWrapper)
            camera.disconnect()

    def capture_img(self, storage_dir, capture_index):
        for camera in self.cameras:
            assert isinstance(camera, CameraWrapper)
            camera.storage_dir = storage_dir

        img_capture_tasks = []

        for camera in self.cameras:
            task = Thread(target=camera.capture_img, args=(capture_index,))
            img_capture_tasks.append(task)

        for task in img_capture_tasks:
            task.start()

        for task in img_capture_tasks:
            task.join()

    def get_camera_on_port(self, port):
        for camera in self.cameras:
            assert isinstance(camera, CameraWrapper)

            if camera.port == port:
                return camera

        return None
