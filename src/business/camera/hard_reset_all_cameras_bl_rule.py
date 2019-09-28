import subprocess
from threading import Lock

from business.camera.exceptions import HardResetNotSupportedException, HardResetException


class HardResetAllCamerasBlRule:
    _cmd_ports_down = 'ykushcmd ykush3 -d a'
    _cmd_ports_up = 'ykushcmd ykush3 -u a'
    _ykush_lock = Lock()

    def execute(self):
        try:
            with self._ykush_lock:
                self._run_subprocess_cmd(cmd=self._cmd_ports_down)
                self._run_subprocess_cmd(cmd=self._cmd_ports_up)

        except Exception as e:
            except_msg = str(e)
            if 'command not found' in except_msg:
                raise HardResetNotSupportedException('ykushcmd not found')

            raise HardResetException(except_msg)

    @staticmethod
    def _run_subprocess_cmd(cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise HardResetException(error)