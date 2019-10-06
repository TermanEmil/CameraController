import logging

from enterprise.scheduling.timelapse import Timelapse


class TimelapseEpisodeFinishedListener:
    def run(self, timelapse: Timelapse, **kwargs):
        msg = '--- {}: timelapse episode finished. Capture index = {}'.format(timelapse.name, timelapse.capture_index)
        logging.info(msg)