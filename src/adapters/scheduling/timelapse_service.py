from business.scheduling.timelapse_bl_rules import *
from enterprise.scheduling.timelapse import Timelapse


class TimelapseService:
    def __init__(
            self,
            create_timelapse_bl_rule: CreateTimelapseBlRule):

        self._create_timelapse_bl_rul = create_timelapse_bl_rule

    def create_timelapse(self, timelapse: Timelapse):
        self._create_timelapse_bl_rul.set_params(dto=timelapse).execute()
