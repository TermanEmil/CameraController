from enterprise.camera_ctrl.camera import Camera


class CameraDto:
    def __init__(self, camera: Camera):
        self.name = camera.name
        self.id = camera.id
        self.summary = camera.summary


class CameraCaptureImgAndDownloadDto:
    def __init__(self, *, real_file_path: str, download_filename: str):
        self.real_file_path = real_file_path
        self.download_filename = download_filename