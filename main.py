import argparse
import logging
from threading import Thread

import gphoto2 as gp

from CameraWrapper import CameraWrapper

# Constants
c_storage_dir = '/Volumes/aps/timelapse/software/captured_images'


def build_argparser():
    parser = argparse.ArgumentParser('Timelapse')

    parser.add_argument('--nb-of-photos', dest='nb_of_photos', type=int, required=False)
    parser.add_argument('--interval', dest='interval', type=int, default=1)

    return parser


def autodetect_all_cameras():
    cameras_name_and_addr = gp.check_result(gp.gp_camera_autodetect())

    # Search ports for camera port name
    port_info_list = gp.PortInfoList()
    port_info_list.load()

    cameras_wrappers = []
    for name, port in cameras_name_and_addr:
        print('Detected camera {0} on port: {1}'.format(name, port))

        camera = gp.Camera()
        idx = port_info_list.lookup_path(port)
        camera.set_port_info(port_info_list[idx])
        camera.init()

        cam_name = '{0}_{1}'.format(name, idx)
        cam_wrapper = CameraWrapper(camera, storage_dir=c_storage_dir, camera_name=cam_name)

        cameras_wrappers.append(cam_wrapper)

    return cameras_wrappers


def capture_img_from_all_cameras(cameras, capture_index=0):
    img_capture_tasks = []
    for camera in cameras:
        task = Thread(target=camera.capture_img, args=(capture_index,))
        img_capture_tasks.append(task)

    for task in img_capture_tasks:
        task.start()

    for task in img_capture_tasks:
        task.join()


def main():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)
    gp.check_result(gp.use_python_logging())

    cam_wrappers = autodetect_all_cameras()
    if len(cam_wrappers) == 0:
        print('No cameras detected')
        return 0
    print('Detected a total of {0} camera(s)\n'.format(len(cam_wrappers)))

    capture_img_from_all_cameras(cam_wrappers, 42)


if __name__ == '__main__':
    main()
