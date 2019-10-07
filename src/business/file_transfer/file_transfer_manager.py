import logging
import subprocess
import threading
from typing import Callable

from business.file_transfer.events import FileTransferEvents
from business.messaging.event_manager import EventManager


class FileTransferManager:
    """
    This is using a script.
    The script is supposed to output some flags followed by some text.
    These flags are then used to detect what happened.
    """

    _transferred_flag = '[copied]'
    _recovered_flag = '[recovered]'
    _error_flag = '[error]'
    _bash_cmd_run_file_transfer = './scripts/run_timelapse_file_transfer.sh'

    def __init__(self, event_manager_provider: Callable[[], EventManager]):
        self._event_manager_provider = event_manager_provider

    def run_in_background(self):
        file_transfer_process = subprocess.Popen(
            self._bash_cmd_run_file_transfer.split(),
            stdout=subprocess.PIPE)

        file_transfer_daemon = threading.Thread(
            target=self._run_in_background_core,
            kwargs={"file_transfer_process": file_transfer_process})

        file_transfer_daemon.start()

    def _run_in_background_core(self, file_transfer_process):
        while True:
            line = file_transfer_process.stdout.readline()
            if not line:
                logging.error("Couldn't run file transfer")
                break

            line = line.decode("utf-8").replace('\n', '')
            self._trigger_events_based_on_msg(msg=line)

    def _trigger_events_based_on_msg(self, msg: str):
        if msg.startswith(self._transferred_flag):
            file = msg.strip(self._transferred_flag)

            self._event_manager_provider().trigger_event(
                FileTransferEvents.FILE_TRANSFERRED,
                kwargs={'file': file})
            return

        if msg.startswith(self._recovered_flag):
            file = msg.strip(self._recovered_flag)

            self._event_manager_provider().trigger_event(
                FileTransferEvents.FILE_RECOVERED,
                kwargs={'file': file})
            return

        if msg.startswith(self._error_flag):
            error_msg = msg.strip(self._error_flag)

            self._event_manager_provider().trigger_event(
                FileTransferEvents.ERROR,
                kwargs={'error': error_msg})
            return