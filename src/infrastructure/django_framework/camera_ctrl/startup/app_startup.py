from camera_ctrl.startup.camera_ctrl_startup import CameraCtrlStartup
from camera_ctrl.startup.file_transfer_startup import FileTransferStartup
from camera_ctrl.startup.scheduling_startup import SchedulingStartup


class AppStartup:
    def __init__(
            self,
            camera_ctrl_startup: CameraCtrlStartup,
            file_transfer_startup: FileTransferStartup,
            scheduling_startup: SchedulingStartup):

        self._startup_objs = [camera_ctrl_startup, file_transfer_startup, scheduling_startup]

    def run(self):
        for startup in self._startup_objs:
            startup.run()