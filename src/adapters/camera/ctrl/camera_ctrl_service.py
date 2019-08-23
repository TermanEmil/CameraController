import os
import typing
import time

from business.camera import exceptions
from business.camera.ctrl.autodetect_bl_rule import AutodetectBlRule
from business.camera.ctrl.capture_img_and_download_bl_rule import CaptureImgAndDownloadBlRule
from business.camera.ctrl.capture_preview_bl_rule import CapturePreviewBlRule
from business.camera.ctrl.get_all_cameras_bl_rule import GetAllCamerasBlRule
from business.camera.ctrl.get_camera_bl_rule import GetCameraBlRule
from business.camera.ctrl.hard_reset_all_cameras_bl_rule import HardResetAllCamerasBlRule
from business.camera.ctrl.reconnect_bl_rule import ReconnectBlRule
from business.camera.ctrl.remove_bl_rule import RemoveBlRule
from enterprise.camera_ctrl.camera_manager import CameraManager
from ..camera_exceptions import CameraNotFound
from .dtos import CameraDto, CameraCaptureImgAndDownloadDto


class CameraCtrlService:
    def __init__(
            self,
            camera_manager: CameraManager,
            autodetect_bl_rule: AutodetectBlRule,
            get_all_cameras_bl_rule: GetAllCamerasBlRule,
            get_camera_bl_rule: GetCameraBlRule,
            remove_bl_rule: RemoveBlRule,
            reconnect_bl_rule: ReconnectBlRule,
            capture_img_and_download_bl_rule: CaptureImgAndDownloadBlRule,
            capture_preview_bl_rule: CapturePreviewBlRule,
            hard_reset_all_cameras_bl_rule: HardResetAllCamerasBlRule):

        self._camera_manager = camera_manager
        self._autodetect_bl_rule = autodetect_bl_rule
        self._get_all_cameras_bl_rule = get_all_cameras_bl_rule
        self._get_camera_bl_rule = get_camera_bl_rule
        self._remove_bl_rule = remove_bl_rule
        self._reconnect_bl_rule = reconnect_bl_rule
        self._capture_img_and_download_bl_rule = capture_img_and_download_bl_rule
        self._capture_preview_bl_rule = capture_preview_bl_rule
        self._hard_reset_all_cameras_bl_rule = hard_reset_all_cameras_bl_rule

    def cameras_autodetect(self):
        self._autodetect_bl_rule.execute()

    def camera_get(self, camera_id: str) -> CameraDto:
        try:
            camera = self._get_camera_bl_rule.set_params(camera_id=camera_id).execute()

        except exceptions.CameraNotFound as e:
            raise CameraNotFound(e)

        return CameraDto(camera)

    def cameras_get_all(self) -> typing.Iterable[CameraDto]:
        cameras = self._get_all_cameras_bl_rule.execute()
        return (CameraDto(camera) for camera in cameras)

    def camera_remove(self, camera_id: str):
        try:
            self._remove_bl_rule.set_params(camera_id=camera_id).execute()

        except exceptions.CameraNotFound as e:
            raise CameraNotFound(e)

    def camera_reconnect(self, camera_id: str):
        try:
            self._reconnect_bl_rule.set_params(camera_id=camera_id).execute()

        except exceptions.CameraNotFound as e:
            raise CameraNotFound(e)

    def camera_capture_img_and_download(self, camera_id: str) -> CameraCaptureImgAndDownloadDto:
        file_path = self._capture_img_and_download_bl_rule.set_params(camera_id=camera_id).execute()

        file_extension = os.path.splitext(file_path)[1][1:]
        download_filename = 'capture_sample{0}.{1}'.format(time.time(), file_extension)

        try:
            return CameraCaptureImgAndDownloadDto(real_file_path=file_path, download_filename=download_filename)

        except exceptions.CameraNotFound as e:
            raise CameraNotFound(e)

    def camera_capture_preview(self, camera_id: str) -> memoryview:
        try:
            frame = self._capture_preview_bl_rule.set_params(camera_id=camera_id).execute()
            return frame

        except exceptions.CameraNotFound as e:
            raise CameraNotFound(e)

    def hard_reset_all_cameras(self, wait_seconds_after_reset: int = None):
        with self._camera_manager.sync_lock:
            self._hard_reset_all_cameras_bl_rule.execute()

            if wait_seconds_after_reset:
                time.sleep(wait_seconds_after_reset)

        self._autodetect_bl_rule.execute()