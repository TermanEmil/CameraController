from business.file_transfer.file_transfer_manager import FileTransferManager


class FileTransferService:
    def __init__(self, file_transfer_manager: FileTransferManager):
        self._file_transfer_manager = file_transfer_manager

    def run_in_background(self):
        self._file_transfer_manager.run_in_background()