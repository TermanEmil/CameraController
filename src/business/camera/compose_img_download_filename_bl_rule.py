import os
import time


class ComposeImgDownloadFilenameBlRule:
    @staticmethod
    def execute(actual_filename: str) -> str:
        file_extension = os.path.splitext(actual_filename)[1][1:]
        now = time.time()
        download_filename = 'capture_sample{0}.{1}'.format(now, file_extension)

        return download_filename