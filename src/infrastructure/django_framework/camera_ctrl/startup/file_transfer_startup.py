import logging

from adapters.file_transfer.event_listeners.file_transfer_error_listener import FileTransferErrorListener
from adapters.file_transfer.event_listeners.file_transferred_listener import FileTransferredListener
from adapters.file_transfer.file_transfer_service import FileTransferService
from business.file_transfer.events import FileTransferEvents
from business.messaging.event_manager import EventManager


class FileTransferStartup:
    def __init__(
            self,
            file_transfer_service: FileTransferService,
            event_manager: EventManager,
            file_transferred_listener: FileTransferredListener,
            file_transfer_error_listener: FileTransferErrorListener):

        self._file_transfer_service = file_transfer_service
        self._event_manager = event_manager

        self._file_transferred_listener = file_transferred_listener
        self._file_transfer_error_listener = file_transfer_error_listener

    def run(self):
        self._register_events()
        self._start_file_transfer()

    def _register_events(self):
        self._event_manager.register(FileTransferEvents.FILE_TRANSFERRED, self._file_transferred_listener.run)
        self._event_manager.register(FileTransferEvents.ERROR, self._file_transfer_error_listener.run)

    def _start_file_transfer(self):
        try:
            self._file_transfer_service.run_in_background()

        except Exception as e:
            logging.error('Failed to start file transfer: {}'.format(e))