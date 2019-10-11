from enterprise.camera_ctrl.camera import Camera


def format_capture_error_msg(camera: Camera, error: str):
    return '{}: Failed to take picture. Error: {}'.format(camera.name, error)
