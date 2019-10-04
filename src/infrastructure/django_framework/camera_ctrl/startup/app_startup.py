from camera_ctrl.startup.camera_ctrl_startup import CameraCtrlStartup
from camera_ctrl.startup.file_transfer_startup import FileTransferStartup
from camera_ctrl.startup.scheduling_startup import SchedulingStartup
from shared.di import obj_graph


class AppStartup:
    def run(self):
        obj_graph().provide(CameraCtrlStartup).run()
        obj_graph().provide(FileTransferStartup).run()
        obj_graph().provide(SchedulingStartup).run()