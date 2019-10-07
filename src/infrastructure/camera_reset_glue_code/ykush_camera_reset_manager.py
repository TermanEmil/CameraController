import subprocess
from threading import Lock

from business.camera.camera_reset_manager import CameraResetManager
from business.camera.exceptions import CameraResetNotSupportedException, CameraResetException


class YkushCameraResetManager(CameraResetManager):
    _cmd_ports_down = 'ykushcmd ykush3 -d a'
    _cmd_ports_up = 'ykushcmd ykush3 -u a'
    _ykush_lock = Lock()

    def reset_all(self):
        try:
            with self._ykush_lock:
                self._run_subprocess_cmd(cmd=self._cmd_ports_down)
                self._run_subprocess_cmd(cmd=self._cmd_ports_up)

        except Exception as e:
            except_msg = str(e)
            if 'command not found' in except_msg:
                raise CameraResetNotSupportedException('ykushcmd not found')

            raise CameraResetException(except_msg)

    @staticmethod
    def _run_subprocess_cmd(cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise CameraResetException(error)