from business.camera_manager import CameraManager


class CameraManagerFactory:
    _instance = None

    @staticmethod
    def get():
        if CameraManagerFactory._instance is None:
            CameraManagerFactory._instance = CameraManager()

        return CameraManagerFactory._instance
