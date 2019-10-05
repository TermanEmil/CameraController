import logging

from adapters.file_transfer.file_transfer_service import FileTransferService
from business.file_transfer.events import FileTransferEvents
from business.messaging.event_manager import EventManager
from camera_ctrl.events.file_transfer.file_transferred import file_transferred_log, FileTransferPersistentLog
from camera_ctrl.events.file_transfer.transfer_error import TransferErrorSendEmail, transfer_error_log, \
    TransferErrorPersistentLog
from shared.di import obj_graph


class FileTransferStartup:
    def __init__(
            self,
            file_transfer_service: FileTransferService,
            event_manager: EventManager):

        self._file_transfer_service = file_transfer_service
        self._event_manager = event_manager

    def run(self):
        self._register_events()
        self._start_file_transfer()

    def _register_events(self):
        file_transfer_persistent_log = obj_graph().provide(FileTransferPersistentLog)
        self._event_manager.register(FileTransferEvents.FILE_TRANSFERRED, file_transferred_log)
        self._event_manager.register(FileTransferEvents.FILE_TRANSFERRED, file_transfer_persistent_log.run)

        transfer_error_persistent_log = obj_graph().provide(TransferErrorPersistentLog)
        transfer_error_send_email = obj_graph().provide(TransferErrorSendEmail)
        self._event_manager.register(FileTransferEvents.ERROR, transfer_error_log)
        self._event_manager.register(FileTransferEvents.ERROR, transfer_error_persistent_log.run)
        self._event_manager.register(FileTransferEvents.ERROR, transfer_error_send_email.run)

    def _start_file_transfer(self):
        try:
            self._file_transfer_service.run_in_background()

        except Exception as e:
            logging.error('Failed to start file transfer: {}'.format(e))