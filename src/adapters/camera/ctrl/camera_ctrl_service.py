import time
import typing
from threading import Lock

from business.camera.camera_reset_manager import CameraResetManager
from business.camera.capture_img_and_download_bl_rule import CaptureImgAndDownloadBlRule
from business.camera.compose_img_download_filename_bl_rule import ComposeImgDownloadFilenameBlRule
from business.camera.get_camera_bl_rule import GetCameraBlRule
from enterprise.camera_ctrl.camera_manager import CameraManager
from .camera_ctrl_settings import CameraCtrlSettings
from .dtos import CameraDto, CameraCaptureImgAndDownloadDto


class CameraCtrlService:
    def __init__(
            self,
            camera_manager: CameraManager,
            get_camera_bl_rule: GetCameraBlRule,
            capture_img_and_download_bl_rule: CaptureImgAndDownloadBlRule,
            camera_reset_manager: CameraResetManager,
            camera_ctrl_settings: CameraCtrlSettings,
            compose_img_download_filename_bl_rule: ComposeImgDownloadFilenameBlRule,):

        self._camera_manager = camera_manager
        self._hard_reset_lock = Lock()

        self._get_camera_bl_rule = get_camera_bl_rule
        self._capture_img_and_download_bl_rule = capture_img_and_download_bl_rule
        self._camera_reset_manager = camera_reset_manager
        self._camera_ctrl_settings = camera_ctrl_settings
        self._compose_img_download_filename_bl_rule = compose_img_download_filename_bl_rule

    def cameras_autodetect(self):
        self._camera_manager.detect_all_cameras()

    def camera_get(self, camera_id: str) -> CameraDto:
        camera = self._get_camera_bl_rule.execute(camera_id)
        return CameraDto(camera)

    def cameras_get_all(self) -> typing.Iterable[CameraDto]:
        return (CameraDto(camera) for camera in self._camera_manager.cameras)

    def camera_remove(self, camera_id: str):
        camera = self._get_camera_bl_rule.execute(camera_id)
        self._camera_manager.remove_camera(camera_id=camera.id)

    def camera_reconnect(self, camera_id: str):
        camera = self._get_camera_bl_rule.execute(camera_id)
        camera.disconnect()

    def camera_capture_img_and_download(self, camera_id: str) -> CameraCaptureImgAndDownloadDto:
        file_path = self._capture_img_and_download_bl_rule.execute(camera_id)
        download_filename = self._compose_img_download_filename_bl_rule.execute(file_path)

        return CameraCaptureImgAndDownloadDto(
            real_file_path=file_path,
            download_filename=download_filename)

    def camera_capture_preview(self, camera_id: str) -> memoryview:
        camera = self._get_camera_bl_rule.execute(camera_id)
        return camera.capture_preview()

    def hard_reset_all_cameras(self):
        with self._hard_reset_lock:
            try:
                with self._camera_manager.all_locks:
                    self._camera_reset_manager.reset_all()
                    time.sleep(self._camera_ctrl_settings.seconds_to_wait_after_hard_reset)

            finally:
                self._camera_manager.detect_all_cameras()