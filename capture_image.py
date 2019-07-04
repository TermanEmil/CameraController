import os
import time

import gphoto2 as gp


def _conditional_log(log_it, text):
    if log_it:
        print(text)


def _create_photo_name(current_photo_name):
    file_name, file_extension = os.path.splitext(current_photo_name)

    # Without the dot
    file_extension = file_extension[1:]

    time_in_mills = int(round(time.time() * 1000))
    return '{0}-{1}.{2}'.format('photo', time_in_mills, file_extension)


def capture_image(options, camera, verbose=True):
    _conditional_log(verbose, 'Capturing image')
    file_device_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))

    photo_name = _create_photo_name(file_device_path.name)
    local_file_path = os.path.join(options['img_storage'], photo_name)

    _conditional_log(verbose, 'Copying img to {0}'.format(local_file_path))

    camera_file = gp.check_result(
        gp.gp_camera_file_get(camera, file_device_path.folder, file_device_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, local_file_path))
    _conditional_log(verbose, 'Image saved to {0}'.format(local_file_path))
