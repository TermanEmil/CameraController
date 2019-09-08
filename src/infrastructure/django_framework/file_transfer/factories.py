from file_transfer.startup import FileTransferStartup
from shared.di import obj_graph


def startup_factory() -> FileTransferStartup:
    return obj_graph().provide(FileTransferStartup)