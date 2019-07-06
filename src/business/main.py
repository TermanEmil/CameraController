import logging
import time

import schedules
from CameraManager import CameraManager
from ScheduleManager import ScheduleManager
from utils.time_utils import now

# Constants
c_storage_dir = '/Users/unicornslayer/Projects/Timelapse/Photos'


def init_logger():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)


def main():
    init_logger()

    camera_manager = CameraManager()
    camera_manager.autodetect_all_cameras()

    if len(camera_manager.cameras) == 0:
        print('No cameras detected')
        return 0

    default_schedule = schedules.CounterSchedule(50, 1.5 * 1000, now())
    schedule_manager = ScheduleManager()

    schedule = schedule_manager.pick_schedule(default_schedule=default_schedule)
    if schedule != default_schedule:
        print('Found existing schedule\n')

    schedule_manager.start_schedule(schedule)

    while True:
        time_until_next_capture = schedule.time_until_next_img_capture()
        if time_until_next_capture is None:
            break

        img_index = schedule.get_next_capture_index()
        time.sleep(time_until_next_capture / 1000)
        camera_manager.capture_img(storage_dir=c_storage_dir, capture_index=img_index)


if __name__ == '__main__':
    main()

