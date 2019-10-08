from camera_ctrl.startup.camera_ctrl_startup import CameraCtrlStartup
from camera_ctrl.startup.file_transfer_startup import FileTransferStartup
from camera_ctrl.startup.scheduling_startup import SchedulingStartup


class AppStartup:
    def __init__(
            self,
            camera_ctrl_startup: CameraCtrlStartup,
            file_transfer_startup: FileTransferStartup,
            scheduling_startup: SchedulingStartup):

        self._camera_ctrl_startup = camera_ctrl_startup
        self._file_transfer_startup = file_transfer_startup
        self._scheduling_startup = scheduling_startup

    def run(self):
        self._camera_ctrl_startup.run()
        self._file_transfer_startup.run()
        self._scheduling_startup.run()