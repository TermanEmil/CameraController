import subprocess
from threading import Lock


class HardResetAllCamerasBlRule:
    _bash_cmd = 'ykushcmd ykush3 --reset'
    _ykush_lock = Lock()

    def execute(self):
        try:
            with self._ykush_lock:
                self._inner_call()

        except Exception as e:
            raise type(e)('ykush: {}'.format(e))

    def _inner_call(self):
        process = subprocess.Popen(self._bash_cmd.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()

        if error:
            raise Exception(error)