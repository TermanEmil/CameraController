#!/usr/bin/env python

# python-gphoto2 - Python interface to libgphoto2
# http://github.com/jim-easterbrook/python-gphoto2
# Copyright (C) 2015-19  Jim Easterbrook  jim@jim-easterbrook.me.uk
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import print_function

import logging
import os
import sys

import gphoto2 as gp


def main():
    logging.basicConfig(format='%(levelname)s: %(name)s: %(message)s', level=logging.WARNING)

    gp.check_result(gp.use_python_logging())
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))

    try:
        print('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))

        local_filepath = os.path.join('/Volumes/aps/timelapse/software/captured_images', file_path.name)
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        print('Copying image to', local_filepath)

        camera_file = gp.check_result(
            gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, local_filepath))
        print('Image saved: {0}'.format(local_filepath))

    finally:
        gp.check_result(gp.gp_camera_exit(camera))

    return 0


if __name__ == "__main__":
    sys.exit(main())
