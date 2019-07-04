import os
import gphoto2 as gp

from async_print import async_print


class CameraWrapper:
    def __init__(self, gp_camera, storage_dir, camera_name):
        assert isinstance(gp_camera, gp.Camera)

        self.gp_camera = gp_camera
        self.storage_dir = storage_dir
        self.camera_name = camera_name

        self.verbose = True

    def __del__(self):
        if self.gp_camera is not None:
            self.gp_camera.exit()

    def capture_img(self, img_index=0):
        self._log('Capturing image')
        file_device_path = gp.check_result(gp.gp_camera_capture(self.gp_camera, gp.GP_CAPTURE_IMAGE))

        photo_name = self._create_img_name(file_device_path.name, img_index)
        local_file_path = os.path.join(self.storage_dir, photo_name)

        camera_file = gp.check_result(
            gp.gp_camera_file_get(
                self.gp_camera,
                file_device_path.folder,
                file_device_path.name,
                gp.GP_FILE_TYPE_NORMAL))

        gp.check_result(gp.gp_file_save(camera_file, local_file_path))
        self._log('Image saved to {0}'.format(local_file_path))

    def _log(self, text):
        if self.verbose:
            async_print('{0}: {1}'.format(self.camera_name, text))

    def _create_img_name(self, device_img_name, img_index):
        file_name, file_extension = os.path.splitext(device_img_name)

        # Without the dot
        file_extension = file_extension[1:]
        return '{0}-{1}.{2}'.format(self.camera_name, img_index, file_extension)
