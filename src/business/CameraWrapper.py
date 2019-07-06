import os
import gphoto2 as gp

from utils.async_print import async_print


class _CameraConnection:
    def __init__(self, camera):
        assert isinstance(camera, gp.Camera)
        self.camera = camera

    def __enter__(self):
        self.camera.init()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.camera.exit()


class CameraWrapper:
    def __init__(self, gp_camera, storage_dir=None, camera_name=None, port=None):
        assert isinstance(gp_camera, gp.Camera)

        self.gp_camera = gp_camera
        self.storage_dir = storage_dir
        self.name = camera_name
        self.port = port

        self.verbose = True

    def capture_img(self, img_index=0):
        assert self.storage_dir is not None

        if not os.path.isdir(self.storage_dir):
            raise Exception('Path: "{0}" does not exist'.format(self.storage_dir))

        with _CameraConnection(self.gp_camera):
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
            async_print('{0}: {1}'.format(self.name, text))

    def _create_img_name(self, device_img_name, img_index):
        file_name, file_extension = os.path.splitext(device_img_name)

        # Without the dot
        file_extension = file_extension[1:]
        return '{0}-{1}.{2}'.format(self.name, img_index, file_extension)
