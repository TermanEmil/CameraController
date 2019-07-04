import logging
import time
from CameraManager import CameraManager

# Constants
c_storage_dir = '/Volumes/aps/timelapse/software/captured_images'


def init_logger():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)


def main():
    init_logger()

    camera_manager = CameraManager()
    camera_manager.autodetect_cameras()

    if len(camera_manager.cameras) == 0:
        print('No cameras detected')
        return 0

    n = 5
    for i in range(n):
        camera_manager.capture_img_from_all(storage_dir=c_storage_dir, capture_index=42)
        if i != n - 1:
            time.sleep(5)


if __name__ == '__main__':
    main()
