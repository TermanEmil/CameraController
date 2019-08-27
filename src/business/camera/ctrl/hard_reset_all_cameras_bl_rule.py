import subprocess
from threading import Lock


class HardResetAllCamerasBlRule:
    _bash_cmd_ports_down = 'ykushcmd ykush3 -d a'
    _bash_cmd_ports_up = 'ykushcmd ykush3 -u a'
    _ykush_lock = Lock()

    def execute(self):
        try:
            with self._ykush_lock:
                self._run_subprocess_cmd(cmd=self._bash_cmd_ports_down)
                self._run_subprocess_cmd(cmd=self._bash_cmd_ports_up)

        except Exception as e:
            raise type(e)('ykush: {}'.format(e))

    @staticmethod
    def _run_subprocess_cmd(cmd):
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise Exception(error)