from camera_ctrl.startup.camera_ctrl_startup import CameraCtrlStartup
from camera_ctrl.startup.file_transfer_startup import FileTransferStartup
from shared.di import obj_graph


class AppStartup:
    def run(self):
        obj_graph().provide(CameraCtrlStartup).run()
        obj_graph().provide(FileTransferStartup).run()